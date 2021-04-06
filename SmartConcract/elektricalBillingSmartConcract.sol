// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
//import "remix_tests.sol"; // this import is automatically injected by Remix.
//import "../contracts/3_Ballot.sol";


contract systemRegulationSmartConcract 
{
   
    mapping (uint=>address) usrAddress;
    mapping (address=>uint) usrIndex;
    mapping (address=>bool) usrRegistration;
    mapping (address=>int)  usrWalletCashBalanceEuro;
    mapping (address=>int)  usrWalletCashBalanceCent;
    
    address ownAddress;
    int ownWalletCashBalanceEuro;
    int ownWalletCashBalanceCent;
    int ownEnergyDistributedOnLine;
    int ownEnergyDistributedOffLine;
    
    
    uint blockNumber;
    uint numberOfUser;
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
    uint T2B=T3B;
    uint T2S=23;
    uint T1B=16;
    uint T1S=16;
    
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
     
    }
    
    function setConsumedEnergy(uint[] memory Wusr, int setPrice) public
    {   
        if (usrRegistration[msg.sender]==true)
        {   
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
    }
    
    
    function moneyProccesingForEnergy() private returns(int [] memory )
    {
        int[] memory usrFinalCost=new int[](numberOfUser+1);
        uint sysPro=sysWac+sysWrc+sysWnc;
        uint sysCon=sysWap+sysWap;
        uint sysProFinalCost;
        uint sysConFinalCost;
        uint sysProBaseCost;
        uint sysConBaseCost;
        uint sysDif;
        uint N=10000;
        uint puX;
        uint puY;

        sysProBaseCost=sysWnp*T1S+sysWac*T2S;
        sysProBaseCost=(sysWnc+sysWrc)*T1B+sysWac*T2B;
        
        if  (sysCon<sysPro)
        {   
            sysDif=sysPro-sysCon;
            sysProFinalCost=sysConBaseCost+T3S*sysDif;
            sysConFinalCost=sysConBaseCost;
            
            ownWalletCashBalanceCent-=int(T3S*sysDif);
            ownWalletCashBalanceEuro=ownWalletCashBalanceCent/100;
            ownEnergyDistributedOnLine=int(sysDif);
        }
        else
        {   
            sysDif=sysCon-sysPro;
            sysProFinalCost=sysProBaseCost;
            sysConFinalCost=sysConBaseCost+T3B*sysDif;
            
            ownWalletCashBalanceCent+=int(T3S*sysDif);
            ownWalletCashBalanceEuro=ownWalletCashBalanceCent/100;
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
            usrFinalCost[i]=((-int (puX*(T1S*usrWnp[i]*T2S*usrWap[i]))+int(puY*(T1B*usrWnc[i]+T2B*usrWac[i]+T1B*usrWrc[i]))))/ int(N);
            usrWalletCashBalanceCent[usrAddress[i]]+=usrFinalCost[i];
            usrWalletCashBalanceEuro[usrAddress[i]]+=usrFinalCost[i]/100;
        }
            
        return (usrFinalCost); 
    }
}
