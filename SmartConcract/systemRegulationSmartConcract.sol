// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
//import "remix_tests.sol"; // this import is automatically injected by Remix.
//import "../contracts/3_Ballot.sol";


contract systemRegulationSmartConcract 
{
<<<<<<< HEAD
   
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
=======
    uint  public blockNumber=0;
    uint N=10000;
    
    //Information abaout owner of system/grid
    address ownAddress;
    
    //Informtion about system/grid
    int systemTariffNumber;
    bool systemWork;
    bool systemOwerLoad;
    bool systemNeedsExtraEnergy;
    uint systemPmax=3000000;

    
    //Information abaut users and requast for power
    mapping (uint=>address) usrAddress;
    mapping (address=>uint) usrIndex;
    mapping (address=>bool) usrRegistration;
    uint numberOfUser;

    uint [] usrPnp; //Array Users Not Regulated production power
    uint [] usrPnc; //Array Users Not Regulated consuption power
    uint [] usrPap; //Array Users Avalible production power from EV and Home Battery
    uint [] usrPac; //Array Users Avalible consuption power from EV and Home Battery
    uint [] usrPrc; //Array Users Requasted consuption power from EV and Home Battery
    uint sysPnp;
    uint sysPnc;
    uint sysPap;
    uint sysPac;
    uint sysPrc; 


    modifier newBlockGenerated
   {
      require(block.number>blockNumber);
      _;
    }


    function changeSystemSettings (bool _systemWork, int _systemTariffNumber) private
    {
        systemWork=_systemWork;
        systemTariffNumber=_systemTariffNumber;
    }


    function automaticRegistrationNewUser(address _address) private 
    {   
        usrRegistration[_address]= true;
        usrIndex[_address]=numberOfUser;
        usrAddress[usrIndex[_address]]=_address;
        numberOfUser+=1;
    }

    function deletionPreviousSentDataOfUsers() private newBlockGenerated
    {
        if (block.number>blockNumber)
>>>>>>> e71b851a379b03cc3a6265c62ea41f0c939741cf
        {
            usrPnp= new uint[](numberOfUser);
            usrPnc= new uint[](numberOfUser);
            usrPap= new uint[](numberOfUser);
            usrPac= new uint[](numberOfUser);
            usrPrc= new uint[](numberOfUser);
            blockNumber=block.number;
<<<<<<< HEAD
=======
            sysPnp=0;
            sysPnc=0;
            sysPap=0;
            sysPac=0;
            sysPrc=0;  
            
            
>>>>>>> e71b851a379b03cc3a6265c62ea41f0c939741cf
        }
     
    }
    
<<<<<<< HEAD
    
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
=======
    function setUserValue(uint [5] memory usrP) public
    {   
        if (usrRegistration[msg.sender]==true)
        {   
            deletionPreviousSentDataOfUsers();
            
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
>>>>>>> e71b851a379b03cc3a6265c62ea41f0c939741cf
        }
        
        else
        {   
<<<<<<< HEAD
            userRegistration(msg.sender);
=======
            automaticRegistrationNewUser(msg.sender);
>>>>>>> e71b851a379b03cc3a6265c62ea41f0c939741cf
        }
    }
    
    function checkMaxPowerSystem() public view returns(uint [3] memory)
    {
<<<<<<< HEAD
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
=======
        uint puPap=0;
        uint puPac=0;
        uint puPrc=0;
        
        if (systemPmax>(sysPnc+sysPac+sysPrc))
        {
            puPac=N;
            puPrc=N;
        }
        else if (systemPmax>(sysPnc+sysPrc))
        {
            puPac=(N*(systemPmax-(sysPnc+sysPrc))/sysPac);
            puPrc=N;
        }
        else if (systemPmax>sysPnc)
        {
            puPac=0;
            puPrc=(N*(systemPmax-(sysPnc))/sysPrc);
        }
        else
        {
            puPac=0;
            puPrc=0;
        }       
        
        
        if (systemPmax>(sysPnp+sysPap))
        {
            puPap=N;
        }  
        
        else if (systemPmax>sysPnp)
        {
            puPap=(N*(systemPmax-sysPnp))/sysPap;
        }
        else
        {
            puPap=0;
        }
        
        return ([puPap,puPac,puPrc]);
>>>>>>> e71b851a379b03cc3a6265c62ea41f0c939741cf

    }
    
    function getUsrValue() public view returns(uint [3] memory)
    {
<<<<<<< HEAD
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
=======
        uint [3] memory puPmax= checkMaxPowerSystem();
        uint sysMaxPap=(sysPap*puPmax[0])/N;
        uint sysMaxPac=(sysPac*puPmax[1])/N;
        uint sysMaxPrc=(sysPrc*puPmax[2])/N;
    
        uint C1=sysPnc;
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
>>>>>>> e71b851a379b03cc3a6265c62ea41f0c939741cf
        }
        
        else if (S1>C2)
        {   
<<<<<<< HEAD
            rP=((S1-C2)/sysPmac)*x;
            getPap=0;
            getPac=usrPac[usrIndex[msg.sender]]*((mP[1]*rP)/(x^2));
            getPrc=usrPrc[usrIndex[msg.sender]]*(mP[2]/x);
=======
            puX=((S1-C2)/sysMaxPac)*N;
            Pap=0;
            Pac=(usrPac[usrIndex[msg.sender]]*puPmax[1]*puX)/(N^2);
            Prc=(usrPrc[usrIndex[msg.sender]]*puPmax[2])/N;
>>>>>>> e71b851a379b03cc3a6265c62ea41f0c939741cf
        }
        
        else if (S2>C2)
        {   
<<<<<<< HEAD
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
=======
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
>>>>>>> e71b851a379b03cc3a6265c62ea41f0c939741cf
    }
}
