import { Component } from '@angular/core';
import { AuthService } from '../../../../core/services/auth.service';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  username = '';
  password = '';

  constructor(private authService: AuthService, private router: Router) {}

  onLogin() {
    this.authService.login(this.username, this.password).subscribe(
      {
        next: (response) => {
          this.router.navigate(['/inventory']);
        }, 
        error: (error) => {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Ocurrio un error al intentar iniciar sesion.",
            allowOutsideClick:false,
            customClass:{
              confirmButton:'btn btn-primary bg-danger'
            }
          });
        }
      }
    );
  }
}
