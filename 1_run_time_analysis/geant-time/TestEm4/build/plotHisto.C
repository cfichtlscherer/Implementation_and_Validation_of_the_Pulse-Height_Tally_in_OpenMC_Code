{
  gROOT->Reset();
  
  // Draw histos filled by Geant4 simulation 
  //   
  TFile f("testem4.root");
    
  TCanvas* c1 = new TCanvas("c1", "  ");

  c1->SetLogy(1);
  c1->cd();
  c1->Update();
  
  TH1D* myHist = (TH1D*)f.Get("1");

  // hist->Print("all");
  // hist->Draw("HIST");    

    //Save histogram as text file
    ofstream myFile("histogram.txt");
    myFile << "BinNo" << "\t"<< "Start" << "\t"<< "End" << "\t"<< "No" << endl; for (Int_t i=1; i<=myHist->GetNbinsX();i++) {

    myFile << i << "\t" <<
    (double)(myHist->GetBinCenter(i))-(double)(myHist->GetBinWidth(i)/2.) << "\t" <<
    (double)(myHist->GetBinCenter(i))+(double)(myHist->GetBinWidth(i)/2.) << "\t" << (double)myHist->GetBinContent(i) << endl; }
    myFile.close(); 
  
}  
