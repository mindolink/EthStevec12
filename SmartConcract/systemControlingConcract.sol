// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
//import "remix_tests.sol"; // this import is automatically injected by Remix.
//import "../contracts/3_Ballot.sol";


contract systemRegulationSmartConcract 
{   
    uint public numberOfUser;
    uint blockNumber=0;
    uint N=10000;   //Per-Unit Multiplay
    uint blockTest=1;
    //Information abaout owner of system/grid
    address OwnAddress;
    
    //Informtion about system/grid
    uint public sysMaxPower=15000;   //[W]
    uint public sysTarNum;
    bool public sysNedEne;
    bool public sysRunSta;

    //Users information
    mapping (uint=>address) usrAddress;
    mapping (address=>uint) usrIndex;
    mapping (address=>bool) usrRegistration;
    
    //User required and desired power
    uint [] usrPdSr=[0];    //Array of User info abaut Not regulated power from diferent sources (Source power from Photo Voltaic, Winde Turbine,etc)
    uint [] usrPdLd=[0];    //Array of User info abaut Not regulated power from diferent loads (Any load power devide except Battery)
    uint [] usrPbAvSr=[0];  //rray of User info abaut Avalible power source from Battery or any other regulated source
    uint [] usrPbAvLd=[0];  //Aray of User info abaut Avalible power load from Battery or any other regulated load
    uint [] usrPbRqLd=[0];  //aray of User info abaut Requasted power load from Batterys or any other regulated load
    
    //System required and desired power
    uint public sysPdSr;       //Total Not regulated power from diferent sources
    uint public sysPdLd;       //Total Not regulated power from diferent loads
    uint public sysPbAvSr;     //Total Avalible power source from Battery or any other regulated source
    uint public sysPbAvLd;     //Total Avalible power load from Battery or any other regulated load
    uint sysPbRqLd;     //Total Requasted power load from Batterys or any other regulated load

    bool [] usrAlredySendData;

    modifier checkNonRegistrationOfUser
    {
      require(usrRegistration[msg.sender]==false);
      _;
    }
    
    modifier checkRegistrationOfUser
    {
      require(usrRegistration[msg.sender]==true);
      _;
    }
    
    
    function autoRegistrationNewUser() public checkNonRegistrationOfUser
    {   
        numberOfUser+=1;
        usrRegistration[msg.sender]= true;
        usrIndex[msg.sender]=numberOfUser;
        usrAddress[usrIndex[msg.sender]]=msg.sender;
        usrPdSr.push(0);
        usrPdLd.push(0);
        usrPbAvSr.push(0);
        usrPbAvLd.push(0);
        usrPbRqLd.push(0);
    
    }
    
    function deletePreviousData() private
    {
        usrPdSr= new uint[](numberOfUser+1);
        usrPdLd= new uint[](numberOfUser+1);
        usrPbAvSr= new uint[](numberOfUser+1);
        usrPbAvLd= new uint[](numberOfUser+1);
        usrPbRqLd= new uint[](numberOfUser+1);
        usrAlredySendData= new bool [](numberOfUser+1);
        
        sysPdSr=0;
        sysPdLd=0;
        sysPbAvSr=0;
        sysPbAvLd=0;
        sysPbRqLd=0;  
    }
    
    function setUserDataPower(uint [] memory P) public checkRegistrationOfUser
    { 
        
        if (block.number>blockNumber)
        {
            blockNumber=block.number;
            deletePreviousData();
        }
        if (usrAlredySendData[usrIndex[msg.sender]]==false)
        {   
            //User safe required and desired power
                
            usrPdSr[usrIndex[msg.sender]]=P[0];   
            usrPdLd[usrIndex[msg.sender]]=P[1];   
            usrPbAvSr[usrIndex[msg.sender]]=P[2];   
            usrPbAvLd[usrIndex[msg.sender]]=P[3];   
            usrPbRqLd[usrIndex[msg.sender]]=P[4]; 
                
            //User add required and desired power in system System variables
                
            sysPdSr+=P[0];
            sysPdLd+=P[1];
            sysPbAvSr+=P[2];
            sysPbAvLd+=P[3];
            sysPbRqLd+=P[4];
            usrAlredySendData[usrIndex[msg.sender]]=true;
                
            if (sysPdSr<(sysPdLd+sysPbRqLd))
            {
            sysNedEne=true;
            }
            else
            {
            sysNedEne=false;
            }
        }
    }

    function getUserDataPower() public view returns(uint [3] memory)
    {
        uint [3] memory puPmax= checkMaxPowerOfSystem();
        uint sysMaxPbAvSr=(sysPbAvSr*puPmax[0])/N;
        uint sysMaxPbAvLd=(sysPbAvLd*puPmax[1])/N;
        uint sysMaxPbRqLd=(sysPbRqLd*puPmax[2])/N;
    
        uint C2=sysPdLd+sysMaxPbAvLd;
        uint C3=sysPdLd+sysMaxPbAvLd+sysMaxPbRqLd;
        uint S1=sysPdSr;      
        uint S2=sysPdSr+sysMaxPbAvSr;
        
        uint puX;
        uint getPbAvSr;
        uint getPbAvLd;
        uint getPbRqLd;
        
        if (S1>C3)
        {
            getPbAvSr=0;
            getPbAvLd=(usrPbAvLd[usrIndex[msg.sender]]*puPmax[1])/N;
            getPbRqLd=(usrPbRqLd[usrIndex[msg.sender]]*puPmax[2])/N;
        }
        
        else if (S1>C2)
        {   
            puX=(N*(S1-C2))/sysMaxPbAvLd;
            getPbAvSr=0;
            getPbAvLd=(usrPbAvLd[usrIndex[msg.sender]]*puPmax[1]*puX)/(N*N);
            getPbRqLd=(usrPbRqLd[usrIndex[msg.sender]]*puPmax[2])/N;
        }
        
        else if (S2>C2)
        {   
            puX=(N*(C2-S1))/sysMaxPbAvSr;
            getPbAvSr=(usrPbAvSr[usrIndex[msg.sender]]*puPmax[0]*puX)/(N*N);
            getPbAvLd=0;
            getPbRqLd=(usrPbRqLd[usrIndex[msg.sender]]*puPmax[2])/N;
        }
        else
        {
            getPbAvSr=(usrPbAvSr[usrIndex[msg.sender]]*puPmax[0])/N;
            getPbAvLd=0;
            getPbRqLd=(usrPbRqLd[usrIndex[msg.sender]]*puPmax[2])/N;
        }

        return ([getPbAvSr,getPbAvLd,getPbRqLd]);
    }


    function checkMaxPowerOfSystem() public view returns(uint [3] memory)
    {
        uint puPbAvSr=0;
        uint puPbAvLd=0;
        uint puPbRqLd=0;
        
        if (sysMaxPower>(sysPdLd+sysPbAvLd+sysPbRqLd))
        {
            puPbAvLd=N;
            puPbRqLd=N;
        }
        else if (sysMaxPower>(sysPdLd+sysPbRqLd))
        {
            puPbAvLd=(N*(sysMaxPower-(sysPdLd+sysPbRqLd)))/sysPbAvLd;
            puPbRqLd=N;
        }
        else if (sysMaxPower>sysPdLd)
        {
            puPbAvLd=0;
            puPbRqLd=(N*(sysMaxPower-(sysPdLd)))/sysPbRqLd;
        }
        else
        {
            puPbAvLd=0;
            puPbRqLd=0;
        }       
        
        if (sysMaxPower>(sysPdSr+sysPbAvSr))
        {
            puPbAvSr=N;
        }  
        
        else if (sysMaxPower>sysPdSr)
        {
            puPbAvSr=(N*(sysMaxPower-sysPdSr))/sysPbAvSr;
        }
        else
        {
            puPbAvSr=0;
        }
        
        return ([puPbAvSr,puPbAvLd,puPbRqLd]);
        
    }

    function modifaySystemTarifeNumber(uint _sysTarNum) public checkRegistrationOfUser
    {
        sysTarNum=_sysTarNum;
    }

    function modifaySystemRunningStatus(bool _sysRunSta) public
    {
        sysRunSta=_sysRunSta;
    }

    function modifaySystemMaxPower(uint _sysMaxPower) public
    {
        sysMaxPower=_sysMaxPower;
    }

    function getUserIndex() public view returns(uint) 
    {
        return(usrIndex[msg.sender]);
    }
    
    function registrationNewUser(address _Address) public checkRegistrationOfUser
    {   
        numberOfUser++;
        usrRegistration[_Address]= true;
        usrIndex[_Address]=numberOfUser++;
        usrAddress[usrIndex[_Address]]=_Address;
    }
    
}