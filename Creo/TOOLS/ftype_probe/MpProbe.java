import com.ptc.pfc.pfcModel.*;
import com.ptc.pfc.pfcSession.*;
import com.ptc.pfc.pfcSolid.*;
import com.ptc.pfc.pfcAsyncConnection.*;
import com.ptc.pfc.pfcPart.*;
import com.ptc.pfc.pfcObject.*;
import com.ptc.pfc.pfcModelItem.*;
import com.ptc.pfc.pfcBase.*;

public class MpProbe {
    static void dump(String title, MassProperty mp) throws Exception {
        System.out.println("--- " + title + " ---");
        System.out.println("GetVolume      = " + mp.GetVolume());
        System.out.println("GetSurfaceArea = " + mp.GetSurfaceArea());
        System.out.println("GetMass        = " + mp.GetMass());
        System.out.println("GetDensity     = " + mp.GetDensity());
    }

    public static void main(String[] args) throws Exception {
        System.out.println("=== JCDFstart ===");
        // pfcasyncmt.dll НУЖНО загрузить ДО pfcasync.jar: именно в ней
        // нативная реализация AsyncConnection_Connect
        System.loadLibrary("pfcasyncmt");
        System.out.println("pfcasyncmt loaded");

        // Подключаемся к УЖЕ РАБОТАЮЩЕМУ CREOSON через AsyncConnection
        AsyncConnection ac = pfcAsyncConnection.AsyncConnection_Connect(
                "127.0.0.1", "8080", "creoson", Integer.valueOf(0));
        Session s = ac.GetSession();
        System.out.println("session ok via AsyncConnection");

        String model = args.length > 0 ? args[0]
            : "Z:\\PTC\\Work\\137.011.0041\\137_011_0041.prt";
        System.out.println("opening: " + model);

        Model m = s.RetrieveModel(pfcModel.ModelDescriptor_Create(
                ModelType.MDL_PART, "", model));
        System.out.println("model: " + m.GetFileName());

        // МАССОВЫЕ СВОЙСТВА ЧЕРЕЗ SOLID
        int solids = 0;
        try {
            ModelItems items = ((ModelItemOwner) m)
                    .ListItems(ModelItemType.ITEM_SOLID_GEOMETRY);
        for (int i = 0; i < items.getarraysize(); i++) {
            ModelItem it = (ModelItem) items.get(i);
            if (!(it instanceof com.ptc.pfc.pfcSolid.Solid)) continue;
            solids++;
            com.ptc.pfc.pfcSolid.Solid sol =
                (com.ptc.pfc.pfcSolid.Solid) it;
                System.out.println("solid #" + solids + " : " + sol.GetFileName());
                dump("  solid massprop", sol.GetMassProperty(""));
                try {
                    SolidBody sb = sol.GetDefaultBody();
                    System.out.println("  body: " + sb.GetName());
                    dump("  body massprop", sb.GetMassProperty(""));
                } catch (Throwable t2) {
                    System.out.println("  body err: " + t2);
                }
            }
        } catch (Throwable t) {
            System.out.println("SOLID ERR: " + t);
            t.printStackTrace();
        }
        System.out.println("solids found: " + solids);
        System.out.println("=== JCDFend ===");
    }
}