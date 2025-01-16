import { Component, ViewChild } from '@angular/core';
import { Product } from '../models/product.model';
import { InventoryService  } from '../inventory.service';
import { AuthService } from '../../core/services/auth.service';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import Swal, { SweetAlertResult } from 'sweetalert2';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-inventory',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './inventory.component.html',
  styleUrl: './inventory.component.scss'
})
export class InventoryComponent {
  products: Product[] = [];
  newProduct: Product = { id: 0, name: '', description: '', category: '', price: 0, stock: 0 };
  isEditMode = false;
  @ViewChild('productForm') productForm!: NgForm;
  
  constructor(private inventoryService: InventoryService, private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    if (typeof window !== 'undefined') {
      this.loadProducts();
      
      const myModalEl = document.getElementById('productModal');
      if(myModalEl){
        myModalEl.addEventListener('show.bs.modal', event => {
          const name = document.getElementById('name');
          if(name){
            setTimeout(() => {
              name.focus();
            }, 500);
          }
        })
      }
    }
  }

  async showErrorMessage(error:string):Promise<SweetAlertResult<any>>{
    return await Swal.fire({
      icon: "error",
      title: "Oops...",
      text: error,
      allowOutsideClick:false,
      customClass:{
        confirmButton:'btn btn-primary bg-danger'
      }
    });
  }

  bloquearPagina():void {
    var overlay = document.getElementById('overlay');
    if(overlay) overlay.hidden = false;
  }
  
  desbloquearPagina():void {
    var overlay = document.getElementById('overlay');
    if(overlay) overlay.hidden = true;
  }

  cerrarModal():void {
    if (this.productForm) {
      this.productForm.resetForm();
    }
    document.getElementById('closeModal')?.click();
  }

  loadProducts(): void {
    this.bloquearPagina();
    this.inventoryService.getProducts().subscribe({
      next: (data: Product[]) => {
        this.products = data;
        this.desbloquearPagina();
      },
      error: (error) => {
        this.showErrorMessage("Ocurrio un error al obtener la lista de productos.");
        this.desbloquearPagina();
      }
    });
  }

  addProduct(): void {
    if (this.newProduct.name && this.newProduct.category && this.newProduct.price) {
      this.bloquearPagina();
      this.inventoryService.addProduct(this.newProduct).subscribe({
        next:(data) => {
          Swal.fire("Producto agregado, ", "", "success");
          this.loadProducts();
          this.resetForm();
          this.desbloquearPagina();
        },
        error:(error) => {
          this.desbloquearPagina();
          if(error.status == 401){
            this.showErrorMessage("Necesitas iniciar sesion de nuevo.").then(()=>{
              this.resetForm();
              this.authService.logout();
              this.router.navigate(['/login']);
            });
          }
          else if(error.status == 400 && error.error && error.error.detail){
            this.showErrorMessage("No se puede agregar el producto: " + error.error.detail);
          }
          else{
            this.showErrorMessage("Ocurrio un error al intentar agregar el producto.");
          }
        }
      });
    }
  }

  editProduct(product: Product): void {
    this.isEditMode = true;
    this.newProduct = JSON.parse(JSON.stringify(product));
  }

  updateProduct(): void {
    if (this.validProduct(this.newProduct)) {
      this.bloquearPagina();
      this.inventoryService.updateProduct(this.newProduct).subscribe({
        next: (response) => {
          Swal.fire(response.message, "", "success");
          this.loadProducts();
          this.resetForm();
          this.desbloquearPagina();
        },
        error: (error) => {
          this.desbloquearPagina();
          if(error.status == 401){
            this.showErrorMessage("Necesitas iniciar sesion de nuevo.").then(()=>{
              this.resetForm();
              this.authService.logout();
              this.router.navigate(['/login']);
            });
          }
          else if(error.status == 400 && error.error && error.error.detail){
            this.showErrorMessage("No se puede actualizar el producto: " + error.error.detail);
          }
          else{
            this.showErrorMessage("Ocurrio un error al intentar actualizar el producto.");
          }
        }
      });
    }
  }

  deleteProduct(id: number): void {
    Swal.fire({
      title: "Estas seguro de querer eliminar el producto?",
      showConfirmButton:false,
      showDenyButton:true,
      showCancelButton: true,
      confirmButtonText: "Eliminar",
      denyButtonText: "Eliminar"
    }).then((result) => {
      if (result.isDenied) {
        console.log('Negado');
        this.inventoryService.deleteProduct(id).subscribe({
          next:(response) => {
            Swal.fire(response.message, "", "success");
            this.loadProducts();
          },
          error:(error) => {
            if(error.status == 401){
              this.showErrorMessage("Necesitas iniciar sesion de nuevo.").then(()=>{
                this.authService.logout();
                this.router.navigate(['/login']);
              });
            }
            else if(error.status == 400 && error.error && error.error.detail){
              this.showErrorMessage("No se puede eliminar el producto: " + error.error.detail);
            }
            else{
              this.showErrorMessage("Ocurrio un error al intentar eliminar el producto. ");
            }
          }
        });
      }
    });
  }

  resetForm(): void {
    this.newProduct = { id: 0, name: '', description: '', category: '', price: 0, stock: 0 };
    this.isEditMode = false;
    this.cerrarModal();
  }

  validProduct(product: Product): boolean {
    if (!product.name || !product.category || !product.price){
      return false;
    }
    return true;
  }
}
