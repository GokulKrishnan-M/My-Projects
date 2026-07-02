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
                            SI.
                          </th>
                          <th>
                            DISTRICT NAME
                          </th>
                           <th>
                            DELETE
                          </th>
                           <th>
                            UPDATE
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                         @foreach($dist as $index => $d)
                            <tr>
                                <td>{{ $index + 1 }}</td>
                                <td>{{ $d->districtname }}</td>
                                <td>
                                    <a href="{{route('deletedist' , ['districtid' => $d->districtid])}}" class="btn btn-sm btn-danger" onclick="return confirm('Are you sure you want to delete this Department?')">Delete</a>
                                </td>
                                <td>
                                    <a href="{{route('updatedist' , ['districtid' => $d->districtid])}}" class="btn btn-sm btn-primary" >Edit</a>
                                </td>
                            </tr>
                        @endforeach
                      </tbody>
                    </table>
                     @if (session('success'))
                  <script>
                    alert('{{session('success') }}')
                  </script>
                  @endif
                  </div>
                </div>
              </div>
            </div>
</div>
</div>

            @endsection