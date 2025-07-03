import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Meal, MealEntry, meals, Nullable } from './data';
import { HttpClient } from '@angular/common/http';

const API_URL = "http://localhost:5000";

@Component({
  selector: 'app-meal-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './meal-form.component.html',
  styleUrls: ['./meal-form.component.css']
})
export class MealFormComponent implements OnInit {
  userId: number = 1;
  data$: Promise<MealEntry[] | undefined> = Promise.resolve(undefined);

  currentMealEntry: Nullable<MealEntry> = {
    timestamp: null,
    count: null,
    meal: null
  };

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get(`${API_URL}/users/${this.userId}`).subscribe((response) => {
      const entries: MealEntry[] = [];
      const res = response as ({id: number, count: number, tiemstamp: number})[];

      for (const value of res) {
        entries.push({
          meal: this.getAllMeals().find((meal) => meal.id == value.id) as Meal,
          count: value.count,
          timestamp: value.count
        })
      }

      this.data$ = Promise.resolve(entries);
    });
  }

  addMeal(mealId: number, count: number, timestamp: number) {
    this.http.post(`${API_URL}/users/${this.userId}`, {
      id: mealId,
      count,
      timestamp
    }).subscribe(async (response) => {
      const mealEntry: MealEntry = {
        meal: meals.find((meal) => meal.id == mealId) as Meal,
        timestamp,
        count
      };

      const data = await this.data$;
      data?.push(mealEntry);

      this.data$ = Promise.resolve(data);
    });
  }

  public deleteMealEntry(mealId: number, timestamp: number) {
    this.http.post(`{API_URL}/users/${this.userId}`, {
      id: mealId,
      timestamp
    }).subscribe(async (response) => {
      let data = await this.data$;
      data = data?.filter((entry) => entry.timestamp != timestamp && entry.meal.id != mealId)

      this.data$ = Promise.resolve(data);
    });
  }

  onSelectMeal(event: Event) {
    if (event.target) {
      const target = event.target as HTMLInputElement;
      this.currentMealEntry.meal = meals.find(meal => meal.id == parseInt(target.value)) as Meal;
    }
  }

  onDateInput(event: Event) {
    if (event.target) {
      const target = event.target as HTMLInputElement;
      const date = new Date(target.value);
      this.currentMealEntry.timestamp = date.getTime();
    }
  }

  getTotalPurine(data: MealEntry[]): number {
    return data.reduce((sum, value) => sum + (value.count * value.meal.purine), 0);
  }

  getComment(data: MealEntry[]): string {
    const total = this.getTotalPurine(data);
    if (total <= 120) return "Gayet sağlıklı bir gün geçirmişsiniz!";
    if (total <= 200) return "Sınırda, dikkatli olmanız iyi olur.";
    return "Bugün biraz fazla pürin almışsınız! Tavsiyeler: Et tüketimini azaltın, sebze artırın.";
  }

  getNonNullMealEntry(): MealEntry {
    const mealEntry: MealEntry = {
      timestamp: this.currentMealEntry.timestamp as number,
      count: this.currentMealEntry.count as number,
      meal: this.currentMealEntry.meal as Meal
    };

    return mealEntry;
  }

  public getAllMeals(): Meal[] {
    return meals;
  }
}
