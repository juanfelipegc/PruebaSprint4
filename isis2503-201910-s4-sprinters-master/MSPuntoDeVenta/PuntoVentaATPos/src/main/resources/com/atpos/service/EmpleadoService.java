package com.atpos.service;

import java.util.ArrayList;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;

import com.atpos.persistence.Persistence;
import com.atpos.vo.VOEmpleado;

@Path("/empleado")
public class EmpleadoService 
{
	
	private Persistence pvs;
	
	public EmpleadoService() {
		pvs = new Persistence();
		// TODO Auto-generated constructor stub
	}

	@GET
	@Produces({javax.ws.rs.core.MediaType.APPLICATION_JSON})
	public ArrayList<VOEmpleado> obtenerEmpleados()
	{
		ArrayList<VOEmpleado> lis = pvs.obtenerEmpleados();
		if(lis != null)
		{
			return lis;
		}
		else
		{
			return new ArrayList<VOEmpleado>();
		}
	}
	
	@POST
	@Consumes({javax.ws.rs.core.MediaType.APPLICATION_JSON})
	public void crearEmpleado(VOEmpleado voe)
	{
		pvs.createEmpleado(voe.getNombre(), 
				voe.getCedula(), 
				voe.getApellido(), 
				voe.getRol(), 
				voe.getEmail(), 
				voe.getSalario());
	}
	

}
