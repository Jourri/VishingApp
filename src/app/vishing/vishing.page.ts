import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-vishing',
  templateUrl: './vishing.page.html',
  styleUrls: ['./vishing.page.scss'],
  standalone: true,
  imports: [CommonModule, RouterModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class VishingPage {
  private apiUrl = 'http://127.0.0.1:8000/predict'; 
  isLoading: boolean = false;
  analysisResult: any = null;

  constructor(private http: HttpClient) {}

  analyzeCall(audioFileOrData: any) {
    this.isLoading = true;
    const formData = new FormData();
    formData.append('file', audioFileOrData);

    this.http.post(this.apiUrl, formData).subscribe({
      next: (response: any) => {
        this.isLoading = false;
        this.analysisResult = response;
        console.log('✅ تم الفحص بنجاح:', response);
      },
      error: (error) => {
        this.isLoading = false;
        console.error('❌ حدث خطأ أثناء الاتصال بالسيرفر:', error);
      }
    });
  }
}