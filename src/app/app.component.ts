import { Component , NgModule} from '@angular/core';
import {HeaderComponent} from './header/header.component'
@NgModule({
  declarations: [
     AppComponent
  ],
  imports: [
    HeaderComponent
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
