import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Pegatinas } from './pegatinas';

describe('Pegatinas', () => {
  let component: Pegatinas;
  let fixture: ComponentFixture<Pegatinas>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Pegatinas]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Pegatinas);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
