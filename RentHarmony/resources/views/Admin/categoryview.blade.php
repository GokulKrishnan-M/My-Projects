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
                            CATEGORY NAME
                          </th>
                          <th>
                            IMAGE
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
                         @foreach($cat as $index => $d)
                            <tr>
                                <td>{{ $index + 1 }}</td>
                                <td>{{ $d->catname }}</td>
                                <td>
                                <img src="{{ asset('/uploads/' . $d->image) }}" class="h-20 w-20 object-cover rounded shadow" alt="Image" 
 style="height: 100px;width:100px;"></td>
                                <td>
                                    <a href="{{route('deletecat' , ['catid' => $d->catid])}}" class="btn btn-sm btn-danger" onclick="return confirm('Are you sure you want to delete this Department?')">Delete</a>
                                </td>
                                <td>
                                    <a href="{{route('updatecat' , ['catid' => $d->catid])}}" class="btn btn-sm btn-primary" >Edit</a>
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
            </div>

            @endsection