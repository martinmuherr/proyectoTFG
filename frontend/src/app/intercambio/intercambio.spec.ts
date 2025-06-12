import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Intercambio } from './intercambio';

describe('Intercambio', () => {
  let component: Intercambio;
  let fixture: ComponentFixture<Intercambio>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Intercambio]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Intercambio);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
