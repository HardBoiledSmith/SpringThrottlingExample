package io.hbsmith;

import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class HelloController {

    @RequestMapping(value = {"/"}, method = RequestMethod.GET)
    public String printHello(ModelMap model) {
        model.addAttribute("message", "hello world 1111111");
        return "hello";
    }

    @RequestMapping(value = {"/home"}, method = RequestMethod.GET)
    public String printHello2(ModelMap model) {
        model.addAttribute("message", "hello world 000000");
        return "hello";
    }
}
