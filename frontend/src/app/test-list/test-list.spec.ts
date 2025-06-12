import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestsList } from './test-list';

describe('TestList', () => {
  let component: TestsList;
  let fixture: ComponentFixture<TestsList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestsList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TestsList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
