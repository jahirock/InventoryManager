import { Component, ElementRef, ViewChild } from '@angular/core';
import { AuthService } from '../../../../core/services/auth.service';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent {
  username = '';
  password = '';
  @ViewChild('userInput') user!: ElementRef;

  constructor(private authService: AuthService, private router: Router) {}

  ngAfterViewInit() {
    this.user.nativeElement.focus();
  }

  onRegister() {
    this.authService.register(this.username, this.password).subscribe({
      next: (response) => {
        Swal.fire({
          icon: "success",
          title: "Exito",
          text: "Se ha registrado el usuario con exito.",
          allowOutsideClick:false,
          customClass:{
            confirmButton:'btn btn-primary bg-primary'
          }
        }).then(()=>{
          this.router.navigate(['/login']);
        });
      },
      error: (error) => {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Ocurrio un error en el registro, intente de nuevo.",
          allowOutsideClick:false,
          customClass:{
            confirmButton:'btn btn-primary bg-danger'
          }
        });
      }
    });
  }

  preventSpaces(event: KeyboardEvent): void {
    if (event.code === 'Space' || event.key === ' ') {
      event.preventDefault();
    }
  }
}
