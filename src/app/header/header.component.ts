import { Component, OnInit , NgModule} from '@angular/core';
import { GraphqlService } from '../graphql.service';
import { UserType } from '../types/user';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  constructor(private service: GraphqlService) {


    
    service.getUsers().subscribe(result => {
      this.users = result.data as UserType[];
    })
    console.log(this.users)
  }
 
  ngOnInit() {
  }
  name="Calories tracker"
  counter=2019
  isLogged: boolean
  public users: UserType[];

  changeTitle(){
    this.name="CALORIES TRACKER"
    this.counter++
  }



}
