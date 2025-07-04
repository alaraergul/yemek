import { Component, inject } from "@angular/core";
import { AuthService } from "./auth.service";
import { CommonModule } from "@angular/common";

@Component({
  templateUrl: "./auth.component.html",
  styleUrl: "./auth.component.css",
  imports: [CommonModule]
})
export class AuthComponent {
  authService = inject(AuthService);

  login(username: string, password: string) {
    this.authService.login(username, password);
  }

  register(username: string, password: string, weight: number) {
    this.authService.register(username, password, weight);
  }

  logout() {
    this.authService.logout();
  }

  get user$() {
    return this.authService.user$;
  }

  get error$() {
    return this.authService.logout();
  }
}
