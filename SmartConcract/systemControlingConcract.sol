// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
//import "remix_tests.sol"; // this import is automatically injected by Remix.
//import "../contracts/3_Ballot.sol";


contract systemRegulationSmartConcract 
{   uint NumberOfUser;
    uint BlockNumber=0;
    uint N=10000;
    
    //Information abaout owner of system/grid
    address ownAddress;
    
    //Informtion about system/grid
    uint SystemMaxPower=400;            //[W]
    uint public SystemPriceTariffNumber;
    bool public SystemNeedsEnergy;
    bool public SystemRuning;


    //Information abaut users and requast for power
    mapping (uint=>address) usrAddress;
    mapping (address=>uint) usrIndex;
    mapping (address=>bool) usrRegistration;

    uint [] usrPnp; //Array Users Not Regulated production power
    uint [] usrPnc; //Array Users Not Regulated consuption power
    uint [] usrPap; //Array Users Avalible production power from EV and Home Battery
    uint [] usrPac; //Array Users Avalible consuption power from EV and Home Battery
    uint [] usrPrc; //Array Users Requasted consuption power from EV and Home Battery
    bool [] usrSendData;
    
    uint sysPnp;
    uint sysPnc;
    uint sysPap;
    uint sysPac;
    uint sysPrc; 


    function automaticRegistrationNewUser(address _address) private 
    {   
        usrRegistration[_address]= true;
        usrIndex[_address]=NumberOfUser;
        usrAddress[usrIndex[_address]]=_address;
        NumberOfUser+=1;
    }

    function deletionPreviousSentDataOfUsers() private
    {
        usrPnp= new uint[](NumberOfUser);
        usrPnc= new uint[](NumberOfUser);
        usrPap= new uint[](NumberOfUser);
        usrPac= new uint[](NumberOfUser);
        usrPrc= new uint[](NumberOfUser);
        usrSendData=new bool [](NumberOfUser);
        sysPnp=0;
        sysPnc=0;
        sysPap=0;
        sysPac=0;
        sysPrc=0;  
    }
    
    function setUserValuePower(uint [5] memory usrP) public
    {   
        if (usrRegistration[msg.sender]==true)
        {   
            if (block.number>BlockNumber)
            {
                BlockNumber=block.number;
                deletionPreviousSentDataOfUsers();
            }
            if (usrSendData[usrIndex[msg.sender]]==false)
            {   //User  safe requast and demand for POwer
                usrPnp[usrIndex[msg.sender]]=usrP[0];   //User unRegulated production power
                usrPnc[usrIndex[msg.sender]]=usrP[1];   //User unRegulated consuption power
                usrPap[usrIndex[msg.sender]]=usrP[2];   //Avalible production power
                usrPac[usrIndex[msg.sender]]=usrP[3];   //Avalible consuption power
                usrPrc[usrIndex[msg.sender]]=usrP[4];   //Reguasted consuption power 
                //Sum system owerall power thro specifich segment
                sysPnp+=usrP[0];
                sysPnc+=usrP[1];
                sysPap+=usrP[2];
                sysPac+=usrP[3];
                sysPrc+=usrP[4];

                if (sysPnp<(sysPnc+sysPrc))
                {
                    SystemNeedsEnergy=true;
                }
                else
                {
                    SystemNeedsEnergy=false;
                }
             } 
        }
        else
        {   
            automaticRegistrationNewUser(msg.sender);
        }
    }
    
    function checkMaxPowerOfSystem() private view returns(uint [3] memory)
    {
        uint puPap=0;
        uint puPac=0;
        uint puPrc=0;
        
        if (SystemMaxPower>(sysPnc+sysPac+sysPrc))
        {
            puPac=N;
            puPrc=N;
        }
        else if (SystemMaxPower>(sysPnc+sysPrc))
        {
            puPac=(N*(SystemMaxPower-(sysPnc+sysPrc))/sysPac);
            puPrc=N;
        }
        else if (SystemMaxPower>sysPnc)
        {
            puPac=0;
            puPrc=(N*(SystemMaxPower-(sysPnc))/sysPrc);
        }
        else
        {
            puPac=0;
            puPrc=0;
        }       
        
        
        if (SystemMaxPower>(sysPnp+sysPap))
        {
            puPap=N;
        }  
        
        else if (SystemMaxPower>sysPnp)
        {
            puPap=(N*(SystemMaxPower-sysPnp))/sysPap;
        }
        else
        {
            puPap=0;
        }
        
        return ([puPap,puPac,puPrc]);

    }
    
    function getUserValuePower() public view returns(uint [3] memory)
    {
        uint [3] memory puPmax= checkMaxPowerOfSystem();
        uint sysMaxPap=(sysPap*puPmax[0])/N;
        uint sysMaxPac=(sysPac*puPmax[1])/N;
        uint sysMaxPrc=(sysPrc*puPmax[2])/N;
    
        uint C2=sysPnc+sysMaxPac;
        uint C3=sysPnc+sysMaxPac+sysMaxPrc;
        uint S1=sysPnp;      
        uint S2=sysPnp+sysMaxPap;
        
        uint puX;
        uint Pap;
        uint Pac;
        uint Prc;
        
        if (S1>C3)
        {
            Pap=0;
            Pac=(usrPac[usrIndex[msg.sender]]*puPmax[1])/N;
            Prc=(usrPrc[usrIndex[msg.sender]]*puPmax[2])/N;
        }
        
        else if (S1>C2)
        {   
            puX=((S1-C2)/sysMaxPac)*N;
            Pap=0;
            Pac=(usrPac[usrIndex[msg.sender]]*puPmax[1]*puX)/(N^2);
            Prc=(usrPrc[usrIndex[msg.sender]]*puPmax[2])/N;
        }
        
        else if (S2>C2)
        {   
            puX=((S2-C2)/sysMaxPap)*N;
            Pap=(usrPap[usrIndex[msg.sender]]*puPmax[0]*puX)/(N^2);
            Pac=0;
            Prc=(usrPrc[usrIndex[msg.sender]]*puPmax[2])/N;
        }
        else
        {
            Pap=(usrPap[usrIndex[msg.sender]]*puPmax[0])/N;
            Pac=0;
            Prc=(usrPrc[usrIndex[msg.sender]]*puPmax[2])/N;
        }

        return ([Pap,Pac,Prc]);
    }

    function modifaySystemPriceTariffNumber(uint _SystemPriceTariffNumber) public
    {
        SystemPriceTariffNumber=_SystemPriceTariffNumber;
    }

    function modifaySystemRunning(bool _SystemRuning) public
    {
        SystemRuning=_SystemRuning;
    }
    SDS

}