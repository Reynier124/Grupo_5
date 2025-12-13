import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MostrarAmigos } from './mostrar-amigos';

describe('MostrarAmigos', () => {
  let component: MostrarAmigos;
  let fixture: ComponentFixture<MostrarAmigos>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MostrarAmigos]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MostrarAmigos);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
