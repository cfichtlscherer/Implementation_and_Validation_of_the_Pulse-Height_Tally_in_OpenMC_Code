//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
/// \file electromagnetic/TestEm4/src/DetectorConstruction.cc
/// \brief Implementation of the DetectorConstruction class
//
//
//

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "DetectorConstruction.hh"

#include "G4Material.hh"
#include "G4Tubs.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

DetectorConstruction::DetectorConstruction()
:G4VUserDetectorConstruction()
{}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

DetectorConstruction::~DetectorConstruction()
{}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4VPhysicalVolume* DetectorConstruction::Construct()
{
  //
  // define a material from its elements.   case 1: chemical molecule
  // 
  G4double a, z;
  G4double density;  
  G4int ncomponents, natoms;
 
  G4Element* Al = new G4Element("Aluminium" ,"Al", z= 13., a= 26.9815384*g/mole);
  G4Element* Na = new G4Element("Sodium"    ,"Na", z= 11., a= 22.989769*g/mole);
  G4Element* I  = new G4Element("Iodine"    ,"I" , z= 53., a= 126.90447*g/mole);
  G4Element* O  = new G4Element("Oxigen"    ,"O" , z= 8. , a= 15.999*g/mole);
//  G4Element* Fe = new G4Element("Iron"      ,"Fe", z= 26., a= 55.845*g/mole);
  G4Element* N  = new G4Element("Nitrogen"  ,"N" , z= 7. , a= 14.0067*g/mole);
    

  G4Material* NaI = 
  new G4Material("SodiumIodide", density= 3.667*g/cm3, ncomponents=2);
  NaI->AddElement(Na, natoms=1);
  NaI->AddElement(I, natoms=1);
  // G4cout << NaI << G4endl; apparently not needed, seems like printing the material
 
  G4Material* Alm = 
  new G4Material("Aluminium", density= 2.7*g/cm3, ncomponents=1);
  Alm->AddElement(Al, natoms=1);

  G4Material* AlO = 
  new G4Material("AluminiumOxide", density= 3.97*g/cm3, ncomponents=2);
  AlO->AddElement(Al, natoms=6);
  AlO->AddElement(O, natoms=4);

//  G4Material* Fem = 
//  new G4Material("Iron", density= 7.874*g/cm3, ncomponents=1);
//  Fem->AddElement(Fe, natoms=1);

  G4Material* Air = 
  new G4Material("Air", density= 0.001225*g/cm3, ncomponents=2);
  Air->AddElement(N, natoms=4);
  Air->AddElement(O, natoms=1);

  //     
  // Container
  //  

  G4double naiz=2.64*cm, alfz=0.05*cm, febz=6.18*cm, aloz=2.64*cm, alz=3.59*cm;

  G4double RminW=0., RmaxW=10.*cm, deltaZW= 25.*cm, PhiminW=0., deltaPhiW=360*degree;

  G4Tubs*  
  solidWorld = new G4Tubs("Air",                          //its name
                   RminW,RmaxW,deltaZW,PhiminW,deltaPhiW);     //its size

  G4LogicalVolume*                         
  logicWorld = new G4LogicalVolume(solidWorld,            //its solid
                                   Air,                   //its material
                                   "Air");                //its name
  G4VPhysicalVolume*                                   
  physiWorld = new G4PVPlacement(0,                        //no rotation
                                 G4ThreeVector(),          //at (0,0,0)
                                 logicWorld,               //its logical volume
                                 "Air",                    //its name
                                 0,                        //its mother  volume
                                 false,                    //no boolean operation
                                 0);                       //copy number
 
  G4double Rmin1=0., Rmax1=2.54*cm, deltaZ1= 0.5*5.08*cm, Phimin1=0., deltaPhi1=360*degree;

  G4Tubs*  
  solidNaI = new G4Tubs("NaI",                          //its name
                   Rmin1,Rmax1,deltaZ1,Phimin1,deltaPhi1);     //its size

  G4LogicalVolume*                         
  logicNaI = new G4LogicalVolume(solidNaI,            //its solid
                                   NaI,                   //its material
                                   "NaI");                //its name
  G4VPhysicalVolume*                                   
  physiNaI = new G4PVPlacement(0,                             //no rotation
                               G4ThreeVector(0, 0, naiz),          //at (0.1,0,0)
                               logicNaI,                     //its logical volume
                               "NaI",                    //its name
                               logicWorld,               //its mother  volume
                               false,                    //no boolean operation
                               0);                       //copy number


  G4double Rmin2=0, Rmax2=2.7*cm, deltaZ2= 0.5*0.1*cm, Phimin2=0., deltaPhi2=360*degree;

  G4Tubs*  
  solidAl = new G4Tubs("Al",                                 //its name
                   Rmin2,Rmax2,deltaZ2,Phimin2,deltaPhi2);     //its size

  G4LogicalVolume*                         
  logicAl = new G4LogicalVolume(solidAl,            //its solid
                                   Alm,                   //its material
                                   "Al");                //its name
  G4VPhysicalVolume*                                   
  physiAl = new G4PVPlacement(0,                             //no rotation
                               G4ThreeVector(0, 0, alfz),          //at (0.1,0,0)
                               logicAl,                     //its logical volume
                               "Al",                    //its name
                               logicWorld,               //its mother  volume
                               false,                    //no boolean operation
                               0);                       //copy number

  
  G4double Rmin3=0, Rmax3=2.7*cm, deltaZ3= 0.5*2.*cm, Phimin3=0., deltaPhi3=360*degree;
  
  G4Tubs*  
  solidFe = new G4Tubs("Fe",                                 //its name
             Rmin3,Rmax3,deltaZ3,Phimin3,deltaPhi3);     //its size
  
  G4LogicalVolume*                         
  logicFe = new G4LogicalVolume(solidFe,            //its solid
                             Alm,                   //its material
                             "Fe");                //its name
  G4VPhysicalVolume*                                   
  physiFe = new G4PVPlacement(0,                             //no rotation
                         G4ThreeVector(0, 0, febz),          //at (0.1,0,0)
                         logicFe,                     //its logical volume
                         "Fe",                    //its name
                         logicWorld,               //its mother  volume
                         false,                    //no boolean operation
                         0);                       //copy number
  
  
  G4double Rmin4=2.54*cm, Rmax4=2.7*cm, deltaZ4= 0.5*5.08*cm, Phimin4=0., deltaPhi4=360*degree;

  G4Tubs*  
  solidAlO = new G4Tubs("AlO",                                 //its name
                   Rmin4,Rmax4,deltaZ4,Phimin4,deltaPhi4);     //its size

  G4LogicalVolume*                         
  logicAlO = new G4LogicalVolume(solidAlO,            //its solid
                                   AlO,                   //its material
                                   "AlO");                //its name
  G4VPhysicalVolume*                                   
  physiAlO = new G4PVPlacement(0,                             //no rotation
                               G4ThreeVector(0, 0, aloz),          //at (0.1,0,0)
                               logicAlO,                     //its logical volume
                               "AlO",                    //its name
                               logicWorld,               //its mother  volume
                               false,                    //no boolean operation
                               0);                       //copy number

  G4double Rmin5=2.7*cm, Rmax5=2.84*cm, deltaZ5= 0.5*7.18*cm, Phimin5=0., deltaPhi5=360*degree;

  G4Tubs*  
  solidAlcas = new G4Tubs("Al",                                 //its name
                   Rmin5,Rmax5,deltaZ5,Phimin5,deltaPhi5);     //its size

  G4LogicalVolume*                         
  logicAlcas = new G4LogicalVolume(solidAlcas,            //its solid
                                   Alm,                   //its material
                                   "Al");                //its name
  G4VPhysicalVolume*                                   
  physiAlcas = new G4PVPlacement(0,                             //no rotation
                               G4ThreeVector(0, 0, alz),          //at (0.1,0,0)
                               logicAlcas,                     //its logical volume
                               "Al",                    //its name
                               logicWorld,               //its mother  volume
                               false,                    //no boolean operation
                               0);                       //copy number

  // Set Scoring Volume, motivated by the example B1
  
  fScoringVolume = logicNaI;


  //
  //always return the physical World
  //  

  //  G4double maxStep = 100, maxLength = 20*cm, maxTime = 0.5*ns, minEkin = 10*MeV;
  //  trackerLV->SetUserLimits(new G4UserLimits(maxStep,                       
  //                                           maxLength,                     
  //                                           maxTime,                       
  //                                           minEkin));                     
  //                                                                             


  return physiWorld;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
