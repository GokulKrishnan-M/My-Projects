@extends('layouts.adminmaster')
@section('content')

<div class="col-lg-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">Striped Table</h4>
                  <p class="card-description">
                    Add class <code>.table-striped</code>
                  </p>
                  <div class="table-responsive">
                    <table class="table table-striped">
                      <thead>
                        <tr>
                          <th>
                            CUSTOMER NAME
                          </th>
                          <th>
                            INSTRUMENT NAME
                          </th>
                           <th>
                            BOOK DATE
                          </th>
                          <th>
                            VIEW MORE
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        @foreach($cust as $index => $d)
                            <tr>
                                <td>{{ $d->cust->custname }}</td>
                               <td>{{ $d->inst->instname }}</td>
                               <td>{{ $d->bookdate }}</td>
                               <td>
                                    <a href="{{ route('viewmorebook', ['bookid' => $d->bookid])}}" class="btn btn-sm btn-primary" >View More</a>
                                </td>
                            </tr>
                        @endforeach
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
</div>
</div>

            @endsection