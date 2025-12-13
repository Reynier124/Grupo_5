import { TestBed } from '@angular/core/testing';

import { ServicioNotificacion } from './servicio-notificacion';

describe('ServicioNotificacion', () => {
  let service: ServicioNotificacion;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ServicioNotificacion);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
