import { Component , NgModule} from '@angular/core';
@NgModule({
  declarations: [
     AppComponent
  ],
  providers: [],
  bootstrap: [AppComponent]
})

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'caloriestracker';
}
