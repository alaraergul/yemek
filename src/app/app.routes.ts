import { Routes } from '@angular/router';
import { MealFormComponent } from './meal-form.component';
import { AuthComponent } from './auth.component';

export const routes: Routes = [
  {path: "purin", component: MealFormComponent},
  {path: "purin/auth", component: AuthComponent}
];
