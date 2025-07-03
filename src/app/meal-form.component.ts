import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Meal, meals } from './data';

@Component({
  selector: 'app-meal-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './meal-form.component.html',
  styleUrls: ['./meal-form.component.css']
})
export class MealFormComponent {
  mealList: Meal[] = meals;
  selectedTime: string = '08:00';
  selectedMealId: number | null = null;

  times: string[] = [
    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
    '12:00', '13:00', '14:00', '15:00', '16:00',
    '17:00', '18:00', '19:00', '20:00', '21:00'
  ];

  selectedMeals = {
    breakfast: [] as Meal[],
    lunch: [] as Meal[],
    dinner: [] as Meal[]
  };

  addMeal() {
    if (this.selectedMealId === null) return;

    const selectedMeal = this.mealList.find(m => m.id === this.selectedMealId);
    if (!selectedMeal) return;

    const hour = parseInt(this.selectedTime.split(':')[0], 10);

    if (hour >= 6 && hour < 12) {
      this.selectedMeals.breakfast.push(selectedMeal);
    } else if (hour >= 12 && hour < 17) {
      this.selectedMeals.lunch.push(selectedMeal);
    } else {
      this.selectedMeals.dinner.push(selectedMeal);
    }

    this.selectedMealId = null;
  }

  getMeals() {
    return this.selectedMeals;
  }

  getTotalPurine(): number {
    return [
      ...this.selectedMeals.breakfast,
      ...this.selectedMeals.lunch,
      ...this.selectedMeals.dinner
    ].reduce((sum, meal) => sum + meal.purine, 0);
  }

  getComment(): string {
    const total = this.getTotalPurine();
    if (total <= 120) return "Gayet sağlıklı bir gün geçirmişsiniz!";
    if (total <= 200) return "Sınırda, dikkatli olmanız iyi olur.";
    return "Bugün biraz fazla pürin almışsınız! Tavsiyeler: Et tüketimini azaltın, sebze artırın.";
  }

  getNamesFor(meals: Meal[]): string {
    return meals.length ? meals.map(f => f.name).join(', ') : 'Yok';
  }
}
