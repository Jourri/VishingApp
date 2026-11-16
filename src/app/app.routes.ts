import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'vishing',
    pathMatch: 'full'
  },
  {
    path: 'vishing',
    loadComponent: () => import('./vishing/vishing.page').then(m => m.VishingPage)
  },
  {
    path: 'history',
    loadComponent: () => import('./history/history.page').then(m => m.HistoryPage)
  },
  {
    path: 'alert',
    loadComponent: () => import('./alert/alert.page').then(m => m.AlertPage)
  }
];