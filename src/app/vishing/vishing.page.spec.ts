import { ComponentFixture, TestBed } from '@angular/core/testing';
import { VishingPage } from './vishing.page';

describe('VishingPage', () => {
  let component: VishingPage;
  let fixture: ComponentFixture<VishingPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(VishingPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
