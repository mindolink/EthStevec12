// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

//import "remix_tests.sol"; // this import is automatically injected by Remix.
//import "../contracts/3_Ballot.sol";

contract electricityBillingConcract {
    
    
    int N=100000;
    mapping(uint => address) usrAddress;
    mapping(address => uint) usrIndex;
    mapping(address => bool) usrRegistration;
    mapping(address => int)  usrWalletNanoCent;
    mapping(address => int)  usrEnergyPriceNanoCent;
    
    address ownAddress;
    uint blockTest=0;
    int  ownWalletNanoCent;
    int  ownEnergyDistributed;
    int  ownEnergyPriceNanoCent;

    int [] usrFinalCost;
    
    int Q=1;
    
    uint blockNumber;
    uint numberOfUser;
    
    int [] usrEdSr;
    int [] usrEdLd;
    int [] usrEbAvSr;
    int [] usrEbAvLd;
    int [] usrEbRqLd;

    int sysEdSr; //Array of User info abaut Not regulated Energy from diferent sources (Source power from Photo Voltaic, Winde Turbine,etc)
    int sysEdLd; //Array of User info abaut Not regulated Energy from diferent loads (Any load power devide except Battery)
    int sysEbAvSr; //Array of User info abaut Avalible Energy source from Battery or any other regulated source
    int sysEbAvLd; //Array of User info abaut Avalible Energy load from Battery or any other regulated load
    int sysEbRqLd; //Array of User info abaut Requasted Energy load from Batterys or any other regulated load

    int TarNum = 3;
    int B3Wh = 8;
    int S3Wh = 24;
    int B2Wh = 8;
    int S2Wh = 24;
    int B1Wh = 16;
    int S1Wh = 16;


    int nano=1000000000;
    
    int nB3Ws=(nano*B3Wh)/3600000; //Buy price Tariff 3 in nanoCent for Ws
    int nS3Ws=(nano*S3Wh)/3600000; //Sell price price Tariff 3 in nanoCent for Ws
    int nB2Ws=(nano*B2Wh)/3600000; //Buy price Tariff 2 in nanoCent for Ws
    int nS2Ws=(nano*S2Wh)/3600000; //Sell price Tariff 2 in nanoCent for Ws
    int nB1Ws=(nano*B1Wh)/3600000; //Buy price Tariff 1 in nanoCent for Ws
    int nS1Ws=(nano*S1Wh)/3600000; //Sell price Tariff 1 in nanoCent for Ws

    function autoRegistrationNewUser(int [] memory E) private
    {   
        usrRegistration[msg.sender]= true;
        usrIndex[msg.sender]=numberOfUser;
        usrAddress[usrIndex[msg.sender]]=msg.sender;
        usrWalletNanoCent[msg.sender]=0;
        usrEnergyPriceNanoCent[msg.sender]=0;
        numberOfUser+=1;
        
        usrEdSr.push(E[0]);
        usrEdLd.push(E[1]);
        usrEbAvSr.push(E[2]);
        usrEbAvLd.push(E[3]);
        usrEbRqLd.push(E[4]);
        
        sysEdSr+=E[0];
        sysEdLd+=E[1];
        sysEbAvSr+=E[2];
        sysEbAvLd+=E[3];
        sysEbRqLd+=E[4];
        
    }
    
    function deletePreviousData() private
    {
        usrEdSr= new int[](numberOfUser);
        usrEdLd= new int[](numberOfUser);
        usrEbAvSr= new int[](numberOfUser);
        usrEbAvLd= new int[](numberOfUser);
        usrEbRqLd= new int[](numberOfUser);
        sysEdSr=0;
        sysEdLd=0;
        sysEbAvSr=0;
        sysEbAvLd=0;
        sysEbRqLd=0;
    }
    
    function userDataEnergy(int[] memory E) public
    {   
        if (usrRegistration[msg.sender]==true)
        {  
            if (blockTest>blockNumber)
            {  
                billingProcesingForEnergy();
                deletePreviousData();
                blockNumber=blockTest;
            }
            
            usrEdSr[usrIndex[msg.sender]]=E[0];   //User unRegulated production power
            usrEdLd[usrIndex[msg.sender]]=E[1];   //User unRegulated consuption power
            usrEbAvSr[usrIndex[msg.sender]]=E[2];   //Avalible production power
            usrEbAvLd[usrIndex[msg.sender]]=E[3];   //Avalible consuption power
            usrEbRqLd[usrIndex[msg.sender]]=E[4];   //Reguasted consuption power 

            sysEdSr+=E[0];
            sysEdLd+=E[1];
            sysEbAvSr+=E[2];
            sysEbAvLd+=E[3];
            sysEbRqLd+=E[4];
        }
        
        else
        {  
            autoRegistrationNewUser(E);
        }
    }


    function userWalletInCent() public view returns(int)
    {
        int CENT=usrWalletNanoCent[msg.sender]/(int(nano));
        
        return(CENT);
    }
    

    function billingProcesingForEnergy() public
    {
        int sysCon=sysEbAvLd+sysEbRqLd+sysEdLd;
        int sysPro=sysEdSr+sysEbAvSr;
        
        int sysProBaseCost;
        int sysConBaseCost;
        int sysProFinalCost;
        int sysConFinalCost;
        int sysDif;
        
        int puPro;
        int puCon;
        
        sysProBaseCost=(sysEdSr*nS1Ws)+(sysEbAvSr*nS2Ws);   
        sysConBaseCost=(sysEdLd+sysEbRqLd)*nB1Ws+sysEbAvLd*nB2Ws;
        
        
        if  (sysCon<sysPro)
        {   
            sysDif=sysPro-sysCon;
            sysProFinalCost=sysConBaseCost+nB3Ws*sysDif;
            sysConFinalCost=sysConBaseCost;
            
            if (sysProBaseCost>0)
            {            
                puPro=(N*sysProFinalCost)/sysProBaseCost;
            }
            else
            {
                puPro=0;
            }
            
            puCon=N;
            
            ownEnergyPriceNanoCent=nB3Ws*sysDif;
            ownWalletNanoCent-=nB3Ws*sysDif;
            ownEnergyDistributed=sysDif;
        }
        else
        {   
            sysDif=sysCon-sysPro;
            sysProFinalCost=sysProBaseCost;
            sysConFinalCost=sysProBaseCost+nS3Ws*sysDif;
            
            puCon=N;
            
            if (sysConBaseCost>0)
            {
                puCon=(N*sysConFinalCost)/sysConBaseCost;
            }
            else
            {
                puCon=(N*sysConFinalCost)/sysConBaseCost;
            }
            
            ownEnergyPriceNanoCent=-nS3Ws*sysDif;
            ownWalletNanoCent+=nS3Ws*sysDif;
            ownEnergyDistributed=sysDif;
        }
        
        for(uint i=0;i<numberOfUser;i++)
        {   
            int usrProPriceNanoCent=((puPro*nS1Ws*usrEdSr[i])/N)+((puPro*nS2Ws*usrEbAvSr[i])/N);
            int usrConPriceNanoCent=((puCon*nB1Ws*usrEdLd[i])/N)+((puCon*nB2Ws*usrEbAvLd[i])/N)+((puCon*nB1Ws*usrEbRqLd[i])/N);
            
            usrEnergyPriceNanoCent[usrAddress[i]]=usrConPriceNanoCent-usrProPriceNanoCent;
            usrWalletNanoCent[usrAddress[i]]+=usrConPriceNanoCent-usrProPriceNanoCent;
        }
        
    }
    
    
    function EnergyPriceNanoCent() public view returns(int)
    {
        return(usrEnergyPriceNanoCent[msg.sender]/nano);
    }
    
    function modifaySysTarifePrice(int _TarNum,int _B3Wh, int _S3Wh) public
    {   
        TarNum=_TarNum;
        S3Wh = _S3Wh;
        B3Wh = _B3Wh;

        B2Wh = B3Wh*(100+Q);
        S2Wh = S3Wh*(100-Q);
        
        B1Wh = B3Wh+((S3Wh-B3Wh)/2);
        S1Wh = B1Wh;

        nB3Ws=(nano*B3Wh)/3600000; //Buy price Tariff 3 in nanoCent for Ws
        nS3Ws=(nano*S3Wh)/3600000; //Sell price price Tariff 3 in nanoCent for Ws
        nB2Ws=(nano*B2Wh)/3600000; //Buy price Tariff 2 in nanoCent for Ws
        nS2Ws=(nano*S2Wh)/3600000; //Sell price Tariff 2 in nanoCent for Ws
        nB1Ws=(nano*B1Wh)/3600000; //Buy price Tariff 1 in nanoCent for Ws
        nS1Ws=(nano*S1Wh)/3600000; //Sell price Tariff 1 in nanoCent for Ws   
    }
    
    
    function changeBlock() public 
    {
        blockTest++;
    }
    
}