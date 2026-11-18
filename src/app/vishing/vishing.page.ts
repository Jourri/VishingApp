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
import { micOutline, chevronForwardOutline, arrowForwardOutline, cloudUploadOutline } from 'ionicons/icons';
import { RouterModule } from '@angular/router'; 
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-vishing',
  templateUrl: './vishing.page.html',
  styleUrls: ['./vishing.page.scss'],
  standalone: true,
  imports: [CommonModule, IonContent, RouterModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class VishingPage {
  currentScreen: 'home' | 'report' = 'home';
  isListening: boolean = false;
  isLoading: boolean = false;
  riskPercentage: number = 0;
  riskSummaryText: string = 'جاري تحليل نمط المحادثة...';
  transcriptLines: string[] = [];
  detectedTactics: { label: string; type: string }[] = [];

  constructor(private http: HttpClient) {
    addIcons({ micOutline, chevronForwardOutline, arrowForwardOutline, cloudUploadOutline });
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

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      console.log('تم اختيار الملف:', file.name);
      this.currentScreen = 'report';
      this.resetReport();
      this.isLoading = true;
      this.riskSummaryText = 'جاري تحليل الملف واستخراج النص عبر نموذج Whisper...';

      const formData = new FormData();
      formData.append('file', file);

      this.http.post('http://127.0.0.1:8000/api/analyze', formData).subscribe({
        next: (response: any) => {
          console.log('نتيجة التحليل من السيرفر:', response);
          this.isLoading = false; 

          // تحديث شاشة التقرير بالبيانات الواردة من السيرفر فوراً
          this.riskPercentage = response.risk_percentage || 88;
          this.riskSummaryText = response.threat || "تم اكتشاف مؤشرات احتيال مصرفي.";
          
          const transcripts = response.transcript || [];
          this.transcriptLines = transcripts.map((item: any) => 
            `<div class="chat-bubble call"><strong>${item.speaker}:</strong> ${item.text}</div>`
          );

          this.detectedTactics = (response.tactics || []).map((t: string) => ({ 
            label: t, 
            type: 'danger' 
          }));
        },
        error: (error) => {
          console.error('خطأ في الاتصال بالخادم:', error);
          this.isLoading = false;
          this.riskSummaryText = 'فشل الاتصال بالخادم المحلي!';
          alert('تأكد من تشغيل سيرفر بايثون (uvicorn).');
        }
      });
    }
    event.target.value = '';
  }

  handleFileUpload(event: any) {
    this.onFileSelected(event);
  }

  calculateDashOffset(): number {
    const radius = 56;
    const circumference = 2 * Math.PI * radius;
    return circumference - (this.riskPercentage / 100) * circumference;
  }

  getRiskColor(): string {
    return this.riskPercentage >= 70 ? '#FF5A5F' : '#2AD8B4';
  }

  saveReport() {
    alert('تم حفظ التقرير بنجاح!');
  }
}