import { ChangeDetectorRef, Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartOptions, ChartType } from 'chart.js';
import { MealEntry } from '../data';

@Component({
  selector: 'app-chart',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  template: `
    <div style="width: 100%; max-width: 400px; height: 300px; margin: auto;">
  <canvas baseChart
    [type]="'line'"
    [data]="lineChartData"
    [options]="lineChartOptions"
    [legend]="lineChartLegend">
  </canvas>
</div>

  `
})
export class ChartComponent implements OnChanges {
  @Input("data") data: Promise<MealEntry[]> | undefined;

  @Input("date") date: {day: number, month: number, year: number}| undefined;

    public lineChartLegend = true;


  public lineChartData: ChartConfiguration<"line">["data"] = {
    labels: [
      "Pazartesi",
      "Salı",
      "Çarşamba",
      "Perşembe",
      "Cuma",
      "Cumartesi",
      "Pazar"
    ],
    datasets: [
      {
        data: [],
        label: 'Pürin',
        fill: true,
        tension: 0.4,
        borderColor: '#f06292',
        backgroundColor: 'rgba(250, 98, 146, 0.2)'
      },
      {
        data: [],
        label: 'Şeker',
        fill: true,
        tension: 0.4,
        borderColor: '#4db6ac',
        backgroundColor: 'rgba(77, 182, 172, 0.2)'
      },
      {
        data: [],
        label: 'Kcal',
        fill: true,
        tension: 0.4,
        borderColor: '#9575cd',
        backgroundColor: 'rgba(149, 117, 205, 0.2)'
      }
    ]
  };

  public lineChartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 12
          }
        }
      },
      tooltip: {
        callbacks: {
          label: (context) => `${context.dataset.label}: ${context.formattedValue}`
        }
      }
    },
    elements: {
      line: {
        borderWidth: 2
      },
      point: {
        radius: 5,
        hoverRadius: 7
      }
    },
    scales: {
      x: {
        ticks: {
          font: {
            size: 12
          }
        },
        grid: {
          display: false
        }
      },
      y: {
        beginAtZero: true,
        ticks: {
          font: {
            size: 12
          }
        }
      }
    }
  };

async ngOnChanges(): Promise<void> {
  const data = await this.data;

  if (!this.date) {
    return;
  }

  const selectedDate = new Date(this.date.year, this.date.month, this.date.day);
  const dayOfWeek = selectedDate.getDay();


    const diffToMonday = (dayOfWeek === 0 ? -6 : 1) - dayOfWeek;

    const monday = new Date(selectedDate);


    monday.setDate(selectedDate.getDate() + diffToMonday);
    monday.setHours(0, 0, 0, 0);

    const sunday = new Date(monday);
    sunday.setDate(monday.getDate() + 6);
    sunday.setHours(23, 59, 59, 999);

    if (data) {
      const purine = Array(7).fill(0);
      const sugar = Array(7).fill(0);
      const kcal = Array(7).fill(0);

      const _data = data.filter((entry) => monday.getTime() <= entry.timestamp && entry.timestamp <= sunday.getTime());

      for (const entry of _data) {
        const value = new Date(entry.timestamp);
        const localDay = new Date(value.getFullYear(), value.getMonth(), value.getDate()).getDay();
        const index = localDay === 0 ? 6 : localDay - 1;


        purine[index] += entry.meal.purine * entry.count;
        sugar[index] += entry.meal.sugar * entry.count;
        kcal[index] += entry.meal.kcal * entry.count;
      }


      this.lineChartData = {
        ...this.lineChartData,
        datasets: [
          {
            ...this.lineChartData.datasets[0],
            data: purine
          },
          {
            ...this.lineChartData.datasets[1],
            data: sugar
          },
          {
            ...this.lineChartData.datasets[2],
            data: kcal
          }
        ]
      };
    }
  }
}
