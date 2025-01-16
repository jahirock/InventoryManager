import { Component, ElementRef, ViewChild } from '@angular/core';
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

  @ViewChild('userInput') user!: ElementRef;

  constructor(private authService: AuthService, private router: Router) {}

  ngAfterViewInit() {
    this.user.nativeElement.focus();
  }

  onLogin() {
    this.authService.login(this.username, this.password).subscribe(
      {
        next: (response) => {
          this.router.navigate(['/inventory']);
        }, 
        error: (error) => {
          var message = 'No se puede iniciar sesion. ';

          if(error.status == 401){
            message += error.error.detail;
          }

          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: message,
            allowOutsideClick:false,
            customClass:{
              confirmButton:'btn btn-primary bg-danger'
            }
          });
        }
      }
    );
  }

  preventSpaces(event: KeyboardEvent): void {
    if (event.code === 'Space' || event.key === ' ') {
      event.preventDefault();
    }
  }

}
