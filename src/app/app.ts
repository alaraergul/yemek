import { Component } from '@angular/core';
import { MealFormComponent } from './meal-form.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MealFormComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {}
