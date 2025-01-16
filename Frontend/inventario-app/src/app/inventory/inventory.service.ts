import { Injectable } from '@angular/core';
import { environment } from '../../enviroments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Product } from './models/product.model';
import { MetaResponse } from '../core/models/meta-response.model';

@Injectable({
  providedIn: 'root'
})
export class InventoryService {
  private baseUrl = environment.apiUrl + '/products';
  
  constructor(private http: HttpClient) { }

  getProducts(skip: number = 0, limit: number = 20): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.baseUrl}/?skip=${skip}&limit=${limit}`);
  }

  addProduct(product: Product): Observable<Product> {
    return this.http.post<Product>(this.baseUrl, product);
  }

  updateProduct(product: Product): Observable<MetaResponse> {
    return this.http.put<MetaResponse>(`${this.baseUrl}`, product);
  }

  deleteProduct(id: number): Observable<MetaResponse> {
    return this.http.delete<MetaResponse>(`${this.baseUrl}/${id}`);
  }

}
