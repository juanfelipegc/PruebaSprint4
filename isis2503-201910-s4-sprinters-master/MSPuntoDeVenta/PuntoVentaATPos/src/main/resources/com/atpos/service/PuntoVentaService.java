package com.atpos.service;


import java.util.ArrayList;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;

import com.atpos.persistence.Persistence;
import com.atpos.vo.VOPuntoVenta;

@Path("/puntoventa")
public class PuntoVentaService 
{
	
	private Persistence pvs;
	
	public PuntoVentaService() 
	{
		pvs = new Persistence();
	}
	@POST
	@Consumes({javax.ws.rs.core.MediaType.APPLICATION_JSON})
	public void crearPuntoVenta(VOPuntoVenta vop)
	{
		pvs.createPuntoVenta(vop.getDireccion(), vop.getNegocio());
	}
	@GET
	@Produces({javax.ws.rs.core.MediaType.APPLICATION_JSON})
	public ArrayList<VOPuntoVenta> obtenerPuntosVenta()
	{
		ArrayList<VOPuntoVenta> l = pvs.obtenerPuntosVenta();
		if(l != null)
		{
			return l;
		}
		else
		{
			return new ArrayList<VOPuntoVenta>();
		}
	}
	

	
}
