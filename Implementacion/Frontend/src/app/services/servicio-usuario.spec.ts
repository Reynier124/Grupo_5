import { TestBed } from '@angular/core/testing';

import { ServicioUsuario } from './servicio-usuario';

describe('Usuario', () => {
  let service: ServicioUsuario;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ServicioUsuario);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
