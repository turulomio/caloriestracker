import { Component, OnInit , NgModule} from '@angular/core';
import { UserType,Query } from '../types/user';
import { Apollo } from 'apollo-angular';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import gql from 'graphql-tag';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  name="Calories tracker"
  counter=2019
  isLogged: boolean
  public users: Observable<Query>
  constructor(private apollo: Apollo) {  }
 
  ngOnInit() {
    this.users = this.apollo.watchQuery<Query>({
      query: gql`query allUsers {
        users {
          nodes {
            id
            name
          }
        }
      }
      `
      
    })
    .valueChanges
;

  }

  changeTitle(){
    this.name="CALORIES TRACKER"
    this.counter++
    console.log(this.users.toString())
    console.log(this.users[0])
  }



}
