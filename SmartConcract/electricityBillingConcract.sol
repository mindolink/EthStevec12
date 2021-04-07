// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
//import "remix_tests.sol"; // this import is automatically injected by Remix.
//import "../contracts/3_Ballot.sol";


contract electricityBillingConcract 
{
   
    mapping (uint=>address) usrAddress;
    mapping (address=>uint) usrIndex;
    mapping (address=>bool) usrRegistration;
    mapping (address=>int)  usrWalletMiliCent;

    
    address ownAddress;
    int ownWalletMiliCent;

    int public ownEnergyDistributed;
    int ownEnergyDistributedOffLine;
    int [] usrFinalCost;
    
    uint public blockNumber;
    uint public numberOfUser;
    uint currentBlockNumber;
    
    uint [] usrWnp;
    uint [] usrWnc;
    uint [] usrWap;
    uint [] usrWac;
    uint [] usrWrc; 
    
    uint sysWnp;    //Array Users Not Regulated production energy
    uint sysWnc;    //Array Users Not Regulated consuption energy
    uint sysWap;    //Array Users Avalible production energy from EV and Home Battery
    uint sysWac;    //Array Users Avalible consuption energy from EV and Home Battery
    uint sysWrc;    //Array Users Requasted consuption energy from EV and Home Battery

    uint T3B=4;
    uint T3S=24;
    uint T2B=6;
    uint T2S=22;
    uint T1B=14;
    uint T1S=14;
    

    modifier ifNewBlockGenerated
    {
      require(block.number>blockNumber);
      _;
    }

    function automaticRegistrationNewUser(address _address) private 
    {   
        usrRegistration[_address]= true;
        usrIndex[_address]=numberOfUser;
        usrAddress[usrIndex[_address]]=_address;
        numberOfUser+=1;
    }
    
    function deletionPreviousSentDataOfUsers() private
    {
            usrWnp= new uint[](numberOfUser);
            usrWnc= new uint[](numberOfUser);
            usrWap= new uint[](numberOfUser);
            usrWac= new uint[](numberOfUser);
            usrWrc= new uint[](numberOfUser);
            sysWnp=0;
            sysWnc=0;
            sysWap=0;
            sysWac=0;
            sysWrc=0;
            blockNumber=block.number;
    }
    
    function setConsumedEnergy(uint[] memory Wusr) public
    {   
        if (usrRegistration[msg.sender]==true)
        {  
            if (block.number>blockNumber)
            {  
                moneyProccesingForEnergy();
                deletionPreviousSentDataOfUsers();
            }
            
            usrWnp[usrIndex[msg.sender]]=Wusr[0];   //User unRegulated production power
            usrWnc[usrIndex[msg.sender]]=Wusr[1];   //User unRegulated consuption power
            usrWap[usrIndex[msg.sender]]=Wusr[2];   //Avalible production power
            usrWac[usrIndex[msg.sender]]=Wusr[3];   //Avalible consuption power
            usrWrc[usrIndex[msg.sender]]=Wusr[4];   //Reguasted consuption power 

            sysWnp=Wusr[0];
            sysWnc=Wusr[1];
            sysWap=Wusr[2];
            sysWac=Wusr[3];
            sysWrc=Wusr[4];
            
        }
        else
        {   
            automaticRegistrationNewUser(msg.sender);
            deletionPreviousSentDataOfUsers();
        }
    }
    function usrFinalCosts()public  view returns(int [] memory)
    {
        return (usrFinalCost);
    }
    
    
    function getUserWalletCashBalance() public view returns (int,int)
    {
        int EURO=usrWalletMiliCent[msg.sender]/100000;
        int CENT=usrWalletMiliCent[msg.sender]/1000;
        
        return(EURO,CENT);
    }
    
    
    function moneyProccesingForEnergy() public
    {
        usrFinalCost=new int[](numberOfUser);
        
        uint sysCon=sysWac+sysWrc+sysWnc;
        uint sysPro=sysWnp+sysWap;
        uint sysProFinalCost;
        uint sysConFinalCost;
        uint sysProBaseCost;
        uint sysConBaseCost;
        uint sysDif;
        uint N=10000;
        uint puX;
        uint puY;

        sysProBaseCost=sysWnp*T1S+sysWap*T2S;   
        sysConBaseCost=(sysWnc+sysWrc)*T1B+sysWac*T2B;
        
        if  (sysCon<sysPro)
        {   
            sysDif=sysPro-sysCon;
            sysProFinalCost=sysConBaseCost+T3S*sysDif;
            sysConFinalCost=sysConBaseCost;
            
            ownWalletMiliCent-=int(T3S*sysDif);
            ownEnergyDistributedOnLine=int(sysDif);
        }
        else
        {   
            sysDif=sysCon-sysPro;
            sysProFinalCost=sysProBaseCost;
            sysConFinalCost=sysConBaseCost+T3B*sysDif;
            
            ownWalletMiliCent+=int(T3S*sysDif);
            ownEnergyDistributedOnLine=-int(sysDif);
        }
    
        if (sysProBaseCost>0)
        {
            puX=(sysProFinalCost/sysProBaseCost)* N;
        }
        else
        {
            puX=0;
        }
            
        if (sysConFinalCost>0)
        {
            puY=(sysConFinalCost/sysConBaseCost)*N;
        }
        else
        {
            puY=0;
        }
            
        for(uint i=0;i<numberOfUser;i++)
        {   
            usrFinalCost[i]=((-int (puX*(T1S*usrWnp[i]*T2S*usrWap[i]))+int(puY*(T1B*usrWnc[i]+T2B*usrWac[i]+T1B*usrWrc[i]))))/ int(N); //[miliCent]
            usrWalletMiliCent[usrAddress[i]]+=usrFinalCost[i];
        }


    }

}