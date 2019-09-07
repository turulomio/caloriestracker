import { Component, OnInit , NgModule} from '@angular/core';
import { GraphqlService } from '../graphql.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  constructor(private service: GraphqlService) {
  }
 
  ngOnInit(): void {
    this.service.getUsers();
  }
  title = 'angulargraphqlclient';
}
