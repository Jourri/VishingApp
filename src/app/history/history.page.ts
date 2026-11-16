import { Component, OnInit, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-history',
  templateUrl: './history.page.html',
  styleUrls: ['./history.page.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class HistoryPage implements OnInit {
  selectedFilter: string = 'all';

  calls = [
    { name: 'مكالمة_بنك_3.01.mp3', time: 'اليوم · 3:42 د', status: 'danger', label: 'خطرة' },
    { name: 'مكالمة_توصيل.wav', time: 'أمس · 1:15 د', status: 'warning', label: 'مشبوهة' },
    { name: 'مكالمة_عائلية.m4a', time: 'قبل يومين · 6:08 د', status: 'safe', label: 'آمنة' },
    { name: 'مكالمة_جوال_3.02.mp3', time: 'قبل 3 أيام · 2:30 د', status: 'danger', label: 'خطرة' },
    { name: 'مكالمة_عمل.wav', time: 'قبل أسبوع · 9:12 د', status: 'safe', label: 'آمنة' },
    { name: 'مكالمة_غريبة.m4a', time: 'قبل أسبوع · 0:48 د', status: 'warning', label: 'مشبوهة' }
  ];

  constructor() {}
  ngOnInit() {}

  get filteredCalls() {
    if (this.selectedFilter === 'all') return this.calls;
    return this.calls.filter(call => call.status === this.selectedFilter);
  }

  setFilter(filter: string) {
    this.selectedFilter = filter;
  }
}