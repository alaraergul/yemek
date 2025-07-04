import { Routes } from '@angular/router';
import { MealFormComponent } from './meal-form.component';
import { AuthComponent } from './auth.component';

export const routes: Routes = [
  {path: "", component: MealFormComponent},
  {path: "auth", component: AuthComponent}
];
