import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestResolver } from './test-resolver';

describe('TestResolver', () => {
  let component: TestResolver;
  let fixture: ComponentFixture<TestResolver>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestResolver]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TestResolver);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
