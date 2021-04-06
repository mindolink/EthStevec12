// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
//import "remix_tests.sol"; // this import is automatically injected by Remix.
//import "../contracts/3_Ballot.sol";


contract systemRegulationSmartConcract 
{
   
    mapping (uint=>address) usrAddress;
    mapping (address=>uint) usrIndex;
    mapping (address=>bool) usrRegistration;
    

    
    uint blockNumber=0;
    uint numberOfUser;
    uint sysNeedsEnergy;
    uint Pmax=20;
    
    uint currentBlockNumber;
    uint currentblockNumber=0;
    
    uint [] usrPnp;
    uint [] public usrPnc;
    uint [] usrPap;
    uint [] usrPac;
    uint [] usrPrc; 
    
    uint sysPnp;    //Array Users Not Regulated production power
    uint sysPnc;    //Array Users Not Regulated consuption power
    uint sysPap;    //Array Users Avalible production power from EV and Home Battery
    uint sysPac;    //Array Users Avalible consuption power from EV and Home Battery
    uint sysPrc;    //Array Users Requasted consuption power from EV and Home Battery


    function userRegistration(address _address) public 
    {   
        usrRegistration[_address]= true;
        usrIndex[_address]=numberOfUser;
        usrAddress[usrIndex[_address]]=_address;
        numberOfUser+=1;
       
    }

    function changeBlockNumber(uint _blockNumber) public
    {
        currentBlockNumber=_blockNumber;
    }



    function deletePreviousValues() private
    {
        if (currentBlockNumber==blockNumber)
        {
            usrPnp= new uint[](numberOfUser);
            usrPnc= new uint[](numberOfUser);
            usrPap= new uint[](numberOfUser);
            usrPac= new uint[](numberOfUser);
            usrPrc= new uint[](numberOfUser);
            blockNumber=block.number;
        }
     
    }
    
    
    function setUserValue(uint [5] memory Pusr) public
    {   
        if (usrRegistration[msg.sender]==true)
        {   
            deletePreviousValues();
            
            usrPnp[usrIndex[msg.sender]]=Pusr[0];   //User unRegulated production power
            usrPnc[usrIndex[msg.sender]]=Pusr[1];   //User unRegulated consuption power
            usrPap[usrIndex[msg.sender]]=Pusr[2];   //Avalible production power
            usrPac[usrIndex[msg.sender]]=Pusr[3];   //Avalible consuption power
            usrPrc[usrIndex[msg.sender]]=Pusr[4];   //Reguasted consuption power 
        
            //Sum system owerall power thro specifich segment
            sysPnp+=Pusr[0];
            sysPnc+=Pusr[1];
            sysPap+=Pusr[2];
            sysPac+=Pusr[3];
            sysPrc+=Pusr[4];                
        }
        
        else
        {   
            userRegistration(msg.sender);
        }
    }
    
    function checkMaxPowerSystem() public view returns(uint [3] memory)
    {
        uint rPap=0;
        uint rPac=0;
        uint rPrc=0;
        uint x=10000;

        if (Pmax>(sysPnc+sysPac+sysPrc))
        {
            rPac=x;
            rPrc=x;
        }
        else if (Pmax>(sysPnc+sysPac))
        {
            rPac=x*((Pmax-(sysPnc+sysPac))/sysPac);
            rPrc=1;
        }
        else
        {
            rPac=0;
            rPrc=x*((Pmax-(sysPnc))/sysPrc);
        }
            
        
        if (Pmax>(sysPnp+sysPap))
        {
            rPap=x;
        }  
        
        else if (Pmax>sysPnp)
        {
            rPap=(x*(Pmax-sysPnp))/sysPap;
        }
        else
        {
            rPap=0;
        }
        
        return ([rPap,rPac,rPrc]);

    }
    
    function getUsrValue() public view returns(uint [3] memory)
    {
        uint [3] memory mP= checkMaxPowerSystem();
        uint x=10000;
        uint sysPmap=(sysPap*mP[0])/x;
        uint sysPmac=(sysPac*mP[1])/x;
        uint sysPmrc=(sysPrc*mP[2])/x;
    
        uint C1=sysPnc;
        uint C2=sysPnc+sysPmac;
        uint C3=sysPnc+sysPmac+sysPmrc;
        uint S1=sysPnp;      
        uint S2=sysPnp+sysPmap;
        
        uint rP;
        uint getPap;
        uint getPac;
        uint getPrc;
        
        if (S1>C3)
        {
            getPap=0;
            getPac=usrPac[usrIndex[msg.sender]]*(mP[1]/x);
            getPrc=usrPrc[usrIndex[msg.sender]]*(mP[2]/x);
        }
        
        else if (S1>C2)
        {   
            rP=((S1-C2)/sysPmac)*x;
            getPap=0;
            getPac=usrPac[usrIndex[msg.sender]]*((mP[1]*rP)/(x^2));
            getPrc=usrPrc[usrIndex[msg.sender]]*(mP[2]/x);
        }
        
        else if (S2>C2)
        {   
            rP=((S2-C2)/sysPmap)*x;
            getPap=usrPap[usrIndex[msg.sender]]*((mP[0]*rP)/(x^2));
            getPac=0;
            getPrc=usrPrc[usrIndex[msg.sender]]*(mP[2]/x);
        }
        else
        {
            rP=((S2-C1)/sysPmrc)*x;
            getPap=usrPap[usrIndex[msg.sender]]*(mP[1]/x);
            getPac=0;
            getPrc=usrPrc[usrIndex[msg.sender]]*(mP[2]/x); 
        }
        return ([getPap,getPac,getPrc]);
    }
}
