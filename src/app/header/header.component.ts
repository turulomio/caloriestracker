import { Component, OnInit , NgModule} from '@angular/core';
import {MenuComponent} from '../menu/menu.component'

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
