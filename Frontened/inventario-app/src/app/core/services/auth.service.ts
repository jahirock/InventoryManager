import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../../enviroments/environment';
import { TokenResponse } from '../models/token-response.model';
import { MetaResponse } from '../models/meta-response.model';
import { response } from 'express';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  
  private baseUrl = environment.apiUrl + '/users';

  constructor(private http: HttpClient) { }

  register(username: string, password: string): Observable<MetaResponse> {
    return this.http.post<MetaResponse>(
      `${this.baseUrl}/register`, 
      { username, password },
      { headers: { 'Content-Type': 'application/json' } }
    );
  }

  login(username: string, password: string): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(
      `${this.baseUrl}/login`, 
      { username, password },
      { headers: { 'Content-Type': 'application/json' } }    
    ).pipe(
      tap(response=>{
        if (response && response.access_token) {
          localStorage.setItem('access_token', response.access_token);
        }
      })
    );
  }
  
  logout(): void {
    localStorage.removeItem('access_token');
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }
}
