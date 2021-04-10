// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract systemRegulationSmartConcract 
{   
    uint public numberOfUser;
    uint blockNumber=0;
    uint N=10000;   //Per-Unit Multiplay
    uint blockTest=1;
    //Information abaout owner of system/grid
    address OwnAddress;
    
    //Informtion about system/grid
    uint sysMaxPower=400;   //[W]
    uint public sysTarNum;
    bool public sysNedEne;
    bool public sysRunSta;

    //Users information
    mapping (uint=>address) usrAddress;
    mapping (address=>uint) usrIndex;
    mapping (address=>bool) usrRegistration;
    
    //User required and desired power
    uint [] usrPdSr;    //Array of User info abaut Not regulated power from diferent sources (Source power from Photo Voltaic, Winde Turbine,etc)
    uint [] usrPdLd;    //Array of User info abaut Not regulated power from diferent loads (Any load power devide except Battery)
    uint [] usrPbAvSr;  //rray of User info abaut Avalible power source from Battery or any other regulated source
    uint [] usrPbAcLd;  //Aray of User info abaut Avalible power load from Battery or any other regulated load
    uint [] usrPbRqLd;  //aray of User info abaut Requasted power load from Batterys or any other regulated load
    
    //System required and desired power
    uint sysPdSr;       //System total Not regulated power from diferent sources
    uint sysPdLd;       //System total Not regulated power from diferent loads
    uint sysPbAvSr;     //System total Avalible power source from Battery or any other regulated source
    uint sysPbAvLd;     //System total Avalible power load from Battery or any other regulated load
    uint sysPbRqLd;     //System total Requasted power load from Batterys or any other regulated load

    bool [] usrSendData;

    modifier checkRegistrationOfUser
    {
      require(usrRegistration[msg.sender]==false);
      _;
    }

    function registrationNewUser(address _Address) public checkRegistrationOfUser
    {   
        numberOfUser++;
        usrRegistration[_Address]= true;
        usrIndex[_Address]=numberOfUser++;
        usrAddress[usrIndex[_Address]]=_Address;
    }
    
    function autoRegistrationNewUser() public checkRegistrationOfUser
    {   
        numberOfUser+=1;
        usrRegistration[msg.sender]= true;
        usrIndex[msg.sender]=numberOfUser;
        usrAddress[usrIndex[msg.sender]]=msg.sender;
    }

    function deletePreviousData() private
    {
        usrPdSr= new uint[](numberOfUser+1);
        usrPdLd= new uint[](numberOfUser+1);
        usrPbAvSr= new uint[](numberOfUser+1);
        usrPbAcLd= new uint[](numberOfUser+1);
        usrPbRqLd= new uint[](numberOfUser+1);
        usrSendData= new bool [](numberOfUser+1);
        
        sysPdSr=0;
        sysPdLd=0;
        sysPbAvSr=0;
        sysPbAvLd=0;
        sysPbRqLd=0;  
    }
    
    function setUserDataPower(uint [5] memory SndReqPower) public
    {   
        if (usrRegistration[msg.sender]==true)
        {   
            if (blockTest>blockNumber)
            {
                blockNumber=blockTest;
                deletePreviousData();
            }
            if (usrSendData[usrIndex[msg.sender]]==false)
            {   
                //User safe required and desired power
                
                usrPdSr[usrIndex[msg.sender]]=SndReqPower[0];   
                usrPdLd[usrIndex[msg.sender]]=SndReqPower[1];   
                usrPbAvSr[usrIndex[msg.sender]]=SndReqPower[2];   
                usrPbAcLd[usrIndex[msg.sender]]=SndReqPower[3];   
                usrPbRqLd[usrIndex[msg.sender]]=SndReqPower[4]; 
                
                //User add required and desired power in system System variables
                
                sysPdSr+=SndReqPower[0];
                sysPdLd+=SndReqPower[1];
                sysPbAvSr+=SndReqPower[2];
                sysPbAvLd+=SndReqPower[3];
                sysPbRqLd+=SndReqPower[4];
                usrSendData[usrIndex[msg.sender]]=true;
                
                
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
        else
        {   
            autoRegistrationNewUser();
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
            getPbAvLd=(usrPbAcLd[usrIndex[msg.sender]]*puPmax[1])/N;
            getPbRqLd=(usrPbRqLd[usrIndex[msg.sender]]*puPmax[2])/N;
        }
        
        else if (S1>C2)
        {   
            puX=(N*(S1-C2))/sysMaxPbAvLd;
            getPbAvSr=0;
            getPbAvLd=(usrPbAcLd[usrIndex[msg.sender]]*puPmax[1]*puX)/(N^2);
            getPbRqLd=(usrPbRqLd[usrIndex[msg.sender]]*puPmax[2])/N;
        }
        
        else if (S2>C2)
        {   
            puX=(N*(S2-C2))/sysMaxPbAvSr;
            getPbAvSr=(usrPbAvSr[usrIndex[msg.sender]]*puPmax[0]*puX)/(N^2);
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

    function modifaySysTarifeNumber(uint _sysTarNum) public
    {
        sysTarNum=_sysTarNum;
    }

    function modifaySysRunningStatus(bool _sysRunSta) public
    {
        sysRunSta=_sysRunSta;
    }

    function changeBlock() public 
    {
        blockTest++;
    }
    
}

