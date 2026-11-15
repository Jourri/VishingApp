import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./vishing/vishing.page').then(m => m.VishingPage)
  },
];