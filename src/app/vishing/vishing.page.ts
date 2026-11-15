/*import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonContent, IonHeader, IonTitle, IonToolbar } from '@ionic/angular';

@Component({
  selector: 'app-vishing',
  templateUrl: './vishing.page.html',
  styleUrls: ['./vishing.page.scss'],
  imports: [IonContent, IonHeader, IonTitle, IonToolbar, CommonModule, FormsModule],
})
export class VishingPage implements OnInit {
  constructor() {}

  ngOnInit() {}
}
*/
import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonContent } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { micOutline, chevronForwardOutline } from 'ionicons/icons';

@Component({
  selector: 'app-vishing',
  templateUrl: './vishing.page.html',
  styleUrls: ['./vishing.page.scss'],
  standalone: true,
  imports: [CommonModule, IonContent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class VishingPage {
  currentScreen: 'home' | 'report' = 'home';
  isListening: boolean = false;
  riskPercentage: number = 0;
  riskSummaryText: string = 'جاري تحليل نمط المحادثة...';
  transcriptLines: string[] = [];
  detectedTactics: { label: string; type: string }[] = [];

  constructor() {
    addIcons({ micOutline, chevronForwardOutline });
  }

  toggleLiveAnalysis() {
    this.isListening = !this.isListening;
    if (this.isListening) {
      this.currentScreen = 'report';
      this.resetReport();
      this.simulateRealTimeCall();
    }
  }

  resetReport() {
    this.riskPercentage = 0;
    this.riskSummaryText = 'جاري الاستماع ورصد التكتيكات...';
    this.transcriptLines = [];
    this.detectedTactics = [];
  }

  simulateRealTimeCall() {
    const steps = [
      { delay: 1000, risk: 35, summary: "تم رصد ادعاء صفة رسمية...", line: `<strong>المتصل:</strong> السلام عليكم، معك موظف من البنك.`, tactics: [{ label: "انتحال صفة", type: "danger" }] },
      { delay: 3000, risk: 87, summary: "طلب خطير (رمز التحقق) - خطورة عالية!", line: `<strong>المتصل:</strong> اعطني رمز التحقق وصلك الحين.`, tactics: [{ label: "طلب OTP", type: "danger" }] }
    ];

    steps.forEach(step => {
      setTimeout(() => {
        if (this.currentScreen === 'report') {
          this.riskPercentage = step.risk;
          this.riskSummaryText = step.summary;
          this.transcriptLines.push(step.line);
          this.detectedTactics = step.tactics;
        }
      }, step.delay);
    });
  }

  handleFileUpload(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.currentScreen = 'report';
      this.resetReport();
      setTimeout(() => { this.simulateRealTimeCall(); }, 1000);
    }
  }

  calculateDashOffset(): number {
    const radius = 56;
    const circumference = 2 * Math.PI * radius;
    return circumference - (this.riskPercentage / 100) * circumference;
  }

  getRiskColor(): string {
    return this.riskPercentage >= 70 ? '#FF5A5F' : '#2AD8B4';
  }
}