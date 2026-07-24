================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### CRITICAL CORE DIRECTIVES (ZERO TOLERANCE)
1. **STRICT FAITHFULNESS TO TEXT**: You are a "clean slate" engineer. Even if you recognize an entity and know more about it from your training data, you MUST NOT add any node, property, or relation that is not stated in the **Input Text**. If a fact is not in the text, it does not exist.
2. **HARD BATCH LIMIT**: You must plan your edits efficiently. **DO NOT EXCEED 20 TOOL CALLS IN A SINGLE ANSWER.** Breaking this limit is a critical system failure. Quality and strict grounding must be achieved within this budget.

### Standardized Identifier & Naming Conventions
To ensure clean downstream entity resolution, all identifiers must follow a uniform, relational-free structure.

#### 1. Core Structural Format
* **Full Formal Name**: Use the most complete, standard name mentioned *within the text* as the identifier basis.
* **Format**: Use `Snake_Case` for all entity identifiers, capitalizing the first letter of each word (e.g., `Julius_Caesar`, `Marcus_Aurelius`).
* **Avoid Pronouns/Aliases**: Never create nodes based on pronouns (`he`, `she`) or temporary descriptions (`the_captain`). Resolve these back to their primary full identifier.

#### 2. NO Relational Suffixes (ABSOLUTE PROHIBITION)
* **NEVER** use familial relations or structural dependencies to construct an identifier string. 
* **PROHIBITED EXAMPLES**: `John_son_of_Robert`, `Mary_daughter_of_Henry`, `Wife_of_Louis_XIV`.
* **Reasoning**: Relational data belongs strictly in the triples (`parentOf`, `spouseOf`), never in the unique node identifier. Incorporating them corrupts entity resolution pipelines.

#### 3. Monarchs, Nobility, and Historic Monickers
* **Regnal Numbers & Monickers**: Include standard regnal numbers or stable historical identifiers *only* if they are explicitly part of their formal name in the text (e.g., `Charlemagne`, `Louis_XIV`, `William_of_Orange`).

#### 4. Disambiguation & Fallbacks (When Identical Names Occur)
If two distinct entities share the exact same name within the text, append a parenthetical qualifier using *only* context provided in the source text:
* **By Role/Attribute**: `Augustus_(Emperor)` vs. `Augustus_(Ship)`.
* **By Category/Profession**: `John_(Apostle)` vs. `John_(Baptist)`.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source (Left)**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it.
* **The Target (Right)**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon.

#### 3. Handling Inverse Property Confusion
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.
* **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
* **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Validate**: Use `ValidateShacl` to check constraints.
4. **Iterate**: Address violations. If a violation (like MinCount) cannot be fixed without hallucinating data not in the text, **ignore the violation**.
5. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **ValidateShacl**: CRITICAL: ALWAYS validate your results before using Finish!
- **Finish**: CRITICAL: ALWAYS use ValidateShacl before finishing!
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Heinrich XIII Prinz Reuss (German: Heinrich XIII.
Prinz Reuß, .mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}pronounced ; born 4 December 1951) is a German businessman, far-right and monarchist activist, and member of the aristocratic – formerly sovereign – House of Reuss.
A proponent of the Reichsbürger movement and antisemitic conspiracy theories, Reuss was arrested by German Federal Police in December 2022 due to his alleged leadership in the 2022 German coup d'état plot.
Biography

Personal life and ancestry

Reuss was born in Büdingen on 4 December 1951, the fifth of six children and the fourth son born to Prince Heinrich I Reuss and Duchess Woizlawa Feodora of Mecklenburg, who was in turn the only child of the German colonial governor Duke Adolf Friedrich of Mecklenburg.
Reuss's parents, like all German nobility, had become private citizens in 1919 upon the adoption of the Weimar Constitution, which abolished any privileges and titles that had previously existed for nobility.
The House of Reuss, from which Reuss is descended, dates to the 12th century and historically administered the regions of Gera and Greiz, a non-contiguous mini-state in what is today Eastern Thuringia.
Reuss left the family association at his own request around 2009.
Reuss married Iranian-born Susan Doukht Jalali in 1989, and they have two children, including a son named Heinrich XXVIII (born circa 1991) and a daughter Elena, who has Down syndrome and was born in 1989.
His wife uses the name Princess Susan Reuss and works as a naturopath.
Reuss is also reported to have as a girlfriend a Russian national identified by prosecutors as "Vitalia B.", aged 39 in 2022, at their arrest who allegedly had some role in the coup plot.
Business and family activities

Reuss worked as a real estate developer, operating a company named Büro Prinz Reuss in Frankfurt, and also produced sparkling wine.
In 1945, the Communist land reform in the Soviet occupation zone (East Germany) expropriated all movable and immovable assets of the House of Reuss.
Following the reunification of Germany in 1990, Reuss tried to have properties restituted.
The clan, which consisted of five large families, wanted Gera townhouses, four castles, extensive forestry and agricultural property and the Jugendstil Reuss Theater in Gera, then held by the city of Gera in Thuringia.
Concerning the theater, Reuss and the mayor of Gera were unable to negotiate a settlement, each blaming the other.
Reuss spent much of his fortune on lawsuits seeking restitution, but with little success.
In 2017, he supported the reinterment of the remains of a number of his ancestors, most prominent among them Henry II, Count of Reuss-Gera, in their original location.
Views and conspiracy theories

Many of Reuss's views are consistent with monarchism.
He has spoken in favour of low flat tax for all citizens and against debt-based business models hailing the 10 percent rate in the former Principality of Reuss, saying it let Reuss's citizens lead "happy lives" because it was "straightforward and transparent".
Reuss contended that the modern German government and European Union were more distant and inaccessible than feudal princes.
Reuss also gave speeches claiming that Germany had been a vassal state since the Second World War.
At World Web Forum in Zürich in 2019, Reuss gave a speech accusing the Rothschilds and Freemasons of responsibility for the wars of the 20th century, expressing antisemitic conspiracy theories.
On 22 December 2018, Reuss and his mother attended the unveiling of a "Flame of Peace" sculpture in Gera in honor of her 100th birthday by the heads of the Vienna-based Association for the Promotion of Peace.
In 2020, Reuss participated in the celebration of the first International Day of Conscience event in Vienna.
Assault on journalist Peter Hagen

In August 2022, Reuss attended an official reception held by Thomas Weigelt, the mayor of Bad Lobenstein, where Reuss's hunting lodge Jagdschloss Waidmannsheil  is located.
Weigelt was known to be sympathetic to the Reichsbürger movement and journalist Peter Hagen asked him why someone associated with the Reichsbürger scene like Reuss would be invited to an official event.
The next day Hagen approached the mayor at the market festival and tried to film him in familiar conversation with Reuss and AfD-politician Uwe Thrum.
Afterwards, the current head of the Reuss family, Heinrich XIV Fürst Reuss , objected to his involvement in local politics "in the strongest possible way".
He called Heinrich XIII, his third cousin, a "distant relative" and "a confused old man peddling in conspiracy theories".
Involvement in 2022 German coup plot

On 7 December 2022, Reuss was arrested at his home in the Westend district of Frankfurt during an extensive raid of alleged far-right conspirators planning a coup d'état.
According to police, the coup's conspirators—which included former Bundestag member Birgit Malsack-Winkemann—were proponents of the Reichsbürger movement who hoped to install the 71-year-old Reuss as head of state Reuss's hunting lodge Jagdschloss Waidmannsheil  in Saaldorf , Thuringia was allegedly the site of weapons stockpiles and meetings regarding the conspiracy.
Reuss and "Vitalia B." are reported to have reached out to the Russian government via its Consulate General in Leipzig, presumably for assistance in the coup.
Heinrich XIV Fürst Reuss distanced himself and his family again after Reuss was arrested in 2022, calling Reuss a "confused old man" and "a marginal figure" and noting that their last common ancestor lived in the early 19th century.
He said Reuss's behaviour was a "catastrophe" for the family, whose heritage as tolerant and cosmopolitan rulers was now associated with "terrorists and reactionaries".
He believes Reuss's anti-government views derive from his resentment at the German judicial system for its failure to recognize his claims to family properties expropriated at the end of World War II.
The trial of Reuss and eight other plotters began on 21 May 2024 in Frankfurt.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix data: <http://example.org/data/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

data:Heinrich_XIII_Prinz_Reuss a :Man ;
    :hasAncestor data:Henry_II_Count_of_Reuss_Gera ;
    :hasBirthYear 1951 ;
    :hasDaughter data:Elena ;
    :hasFather data:Heinrich_I_Reuss,
        data:Susan_Doukht_Jalali ;
    :hasMother data:Woizlawa_Feodora_of_Mecklenburg ;
    :hasSon data:Heinrich_XXVIII .

data:Heinrich_XIV_Fuerst_Reuss a :Man .

data:Vitalia_B a :Woman .

data:Adolf_Friedrich_of_Mecklenburg a :Man .

data:Elena a :Woman ;
    :hasMother data:Susan_Doukht_Jalali .

data:Heinrich_I_Reuss a :Man .

data:Heinrich_XXVIII a :Man ;
    :hasMother data:Susan_Doukht_Jalali .

data:Henry_II_Count_of_Reuss_Gera a :Man .

data:Woizlawa_Feodora_of_Mecklenburg a :Woman ;
    :hasFather data:Adolf_Friedrich_of_Mecklenburg .

data:Susan_Doukht_Jalali a :Woman .



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  RemoveTriple (fd6e67ef-e1cc-44b6-b27a-95c2bd372420)
 Call ID: fd6e67ef-e1cc-44b6-b27a-95c2bd372420
  Args:
    target: data:Susan_Doukht_Jalali
    relation: :hasFather
    source: data:Heinrich_XIII_Prinz_Reuss

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Heinrich_XIII_Prinz_Reuss a :Man ;
      :hasAncestor data:Henry_II_Count_of_Reuss_Gera ;
      :hasBirthYear 1951 ;
      :hasDaughter data:Elena ;
      :hasFather data:Heinrich_I_Reuss ;
      :hasMother data:Woizlawa_Feodora_of_Mecklenburg ;
      :hasSon data:Heinrich_XXVIII .

  data:Heinrich_XIV_Fuerst_Reuss a :Man .

  data:Vitalia_B a :Woman .

  data:Adolf_Friedrich_of_Mecklenburg a :Man .

  data:Elena a :Woman ;
      :hasMother data:Susan_Doukht_Jalali .

  data:Heinrich_I_Reuss a :Man .

  data:Heinrich_XXVIII a :Man ;
      :hasMother data:Susan_Doukht_Jalali .

  data:Henry_II_Count_of_Reuss_Gera a :Man .

  data:Woizlawa_Feodora_of_Mecklenburg a :Woman ;
      :hasFather data:Adolf_Friedrich_of_Mecklenburg .

  data:Susan_Doukht_Jalali a :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AddTriple (31f39288-4d32-4fcc-bbf2-67040270ff1c)
 Call ID: 31f39288-4d32-4fcc-bbf2-67040270ff1c
  Args:
    source: data:Elena
    relation: :hasFather
    target: data:Heinrich_XIII_Prinz_Reuss

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Heinrich_XIV_Fuerst_Reuss a :Man .

  data:Vitalia_B a :Woman .

  data:Adolf_Friedrich_of_Mecklenburg a :Man .

  data:Elena a :Woman ;
      :hasFather data:Heinrich_XIII_Prinz_Reuss ;
      :hasMother data:Susan_Doukht_Jalali .

  data:Heinrich_I_Reuss a :Man .

  data:Heinrich_XIII_Prinz_Reuss a :Man ;
      :hasAncestor data:Henry_II_Count_of_Reuss_Gera ;
      :hasBirthYear 1951 ;
      :hasDaughter data:Elena ;
      :hasFather data:Heinrich_I_Reuss ;
      :hasMother data:Woizlawa_Feodora_of_Mecklenburg ;
      :hasSon data:Heinrich_XXVIII .

  data:Heinrich_XXVIII a :Man ;
      :hasMother data:Susan_Doukht_Jalali .

  data:Henry_II_Count_of_Reuss_Gera a :Man .

  data:Woizlawa_Feodora_of_Mecklenburg a :Woman ;
      :hasFather data:Adolf_Friedrich_of_Mecklenburg .

  data:Susan_Doukht_Jalali a :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AddTriple (d37ca3de-3202-4301-9a26-d91595e547c8)
 Call ID: d37ca3de-3202-4301-9a26-d91595e547c8
  Args:
    relation: :hasFather
    target: data:Heinrich_XIII_Prinz_Reuss
    source: data:Heinrich_XXVIII

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Heinrich_XIV_Fuerst_Reuss a :Man .

  data:Vitalia_B a :Woman .

  data:Adolf_Friedrich_of_Mecklenburg a :Man .

  data:Elena a :Woman ;
      :hasFather data:Heinrich_XIII_Prinz_Reuss ;
      :hasMother data:Susan_Doukht_Jalali .

  data:Heinrich_I_Reuss a :Man .

  data:Heinrich_XXVIII a :Man ;
      :hasFather data:Heinrich_XIII_Prinz_Reuss ;
      :hasMother data:Susan_Doukht_Jalali .

  data:Henry_II_Count_of_Reuss_Gera a :Man .

  data:Woizlawa_Feodora_of_Mecklenburg a :Woman ;
      :hasFather data:Adolf_Friedrich_of_Mecklenburg .

  data:Heinrich_XIII_Prinz_Reuss a :Man ;
      :hasAncestor data:Henry_II_Count_of_Reuss_Gera ;
      :hasBirthYear 1951 ;
      :hasDaughter data:Elena ;
      :hasFather data:Heinrich_I_Reuss ;
      :hasMother data:Woizlawa_Feodora_of_Mecklenburg ;
      :hasSon data:Heinrich_XXVIII .

  data:Susan_Doukht_Jalali a :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (2aff14ee-01aa-4fb7-b000-16f7aace0def)
 Call ID: 2aff14ee-01aa-4fb7-b000-16f7aace0def
  Args:

================================= Tool Message =================================

VALIDATION RESULTS
Total violations:24
Violations:

  Violation [1]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Heinrich_XIII_Prinz_Reuss is assigned as the father of Elena, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Heinrich_XIII_Prinz_Reuss', class=':Ancestor')


  Violation [2]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Adolf_Friedrich_of_Mecklenburg is assigned as the father of Woizlawa_Feodora_of_Mecklenburg, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Adolf_Friedrich_of_Mecklenburg', class=':Ancestor')


  Violation [3]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Susan_Doukht_Jalali is assigned as the mother of Elena, but she is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Susan_Doukht_Jalali', class=':Ancestor')


  Violation [4]:
    SHACL message: Value does not have class :Ancestor
    LLM-provided explanation of the violation:
      The node Henry_II_Count_of_Reuss_Gera is defined as an ancestor of Heinrich_XIII_Prinz_Reuss, but he is missing the required :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Henry_II_Count_of_Reuss_Gera', class=':Ancestor')


  Violation [5]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Heinrich_XIII_Prinz_Reuss is assigned as the father of Heinrich_XXVIII, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Heinrich_XIII_Prinz_Reuss', class=':Ancestor')


  Violation [6]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Heinrich_I_Reuss is assigned as the father of Heinrich_XIII_Prinz_Reuss, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Heinrich_I_Reuss', class=':Ancestor')


  Violation [7]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Susan_Doukht_Jalali is assigned as the mother of Heinrich_XXVIII, but she is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Susan_Doukht_Jalali', class=':Ancestor')


  Violation [8]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Woizlawa_Feodora_of_Mecklenburg is assigned as the mother of Heinrich_XIII_Prinz_Reuss, but she is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Woizlawa_Feodora_of_Mecklenburg', class=':Ancestor')


  Violation [9]:
    SHACL message: Value does not have class :Ancestor
    LLM-provided explanation of the violation:
      The node Henry_II_Count_of_Reuss_Gera is defined as an ancestor of Heinrich_XIII_Prinz_Reuss, but he is missing the required :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Henry_II_Count_of_Reuss_Gera', class=':Ancestor')


  Violation [10]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Adolf_Friedrich_of_Mecklenburg is assigned as the father of Woizlawa_Feodora_of_Mecklenburg, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Adolf_Friedrich_of_Mecklenburg', class=':Ancestor')


  Violation [11]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Heinrich_I_Reuss is assigned as the father of Heinrich_XIII_Prinz_Reuss, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Heinrich_I_Reuss', class=':Ancestor')


  Violation [12]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Heinrich_XIII_Prinz_Reuss is assigned as the father of Elena, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Heinrich_XIII_Prinz_Reuss', class=':Ancestor')


  Violation [13]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Heinrich_XIII_Prinz_Reuss is assigned as the father of Heinrich_XXVIII, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Heinrich_XIII_Prinz_Reuss', class=':Ancestor')


  Violation [14]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Woizlawa_Feodora_of_Mecklenburg is assigned as the mother of Heinrich_XIII_Prinz_Reuss, but she is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Woizlawa_Feodora_of_Mecklenburg', class=':Ancestor')


  Violation [15]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Susan_Doukht_Jalali is assigned as the mother of Elena, but she is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Susan_Doukht_Jalali', class=':Ancestor')


  Violation [16]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Susan_Doukht_Jalali is assigned as the mother of Heinrich_XXVIII, but she is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Susan_Doukht_Jalali', class=':Ancestor')


  Violation [17]:
    SHACL message: Value does not have class :Ancestor
    LLM-provided explanation of the violation:
      The node Henry_II_Count_of_Reuss_Gera is defined as an ancestor of Heinrich_XIII_Prinz_Reuss, but he is missing the required :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Henry_II_Count_of_Reuss_Gera', class=':Ancestor')


  Violation [18]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Adolf_Friedrich_of_Mecklenburg is assigned as the father of Woizlawa_Feodora_of_Mecklenburg, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Adolf_Friedrich_of_Mecklenburg', class=':Ancestor')


  Violation [19]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Heinrich_I_Reuss is assigned as the father of Heinrich_XIII_Prinz_Reuss, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Heinrich_I_Reuss', class=':Ancestor')


  Violation [20]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Heinrich_XIII_Prinz_Reuss is assigned as the father of Elena, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Heinrich_XIII_Prinz_Reuss', class=':Ancestor')


  Violation [21]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Heinrich_XIII_Prinz_Reuss is assigned as the father of Heinrich_XXVIII, but he is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Heinrich_XIII_Prinz_Reuss', class=':Ancestor')


  Violation [22]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Woizlawa_Feodora_of_Mecklenburg is assigned as the mother of Heinrich_XIII_Prinz_Reuss, but she is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Woizlawa_Feodora_of_Mecklenburg', class=':Ancestor')


  Violation [23]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Susan_Doukht_Jalali is assigned as the mother of Elena, but she is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Susan_Doukht_Jalali', class=':Ancestor')


  Violation [24]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Susan_Doukht_Jalali is assigned as the mother of Heinrich_XXVIII, but she is missing the mandatory :Ancestor class.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Susan_Doukht_Jalali', class=':Ancestor')




================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (c17255bd-8a19-4e31-a960-4235911460fe)
 Call ID: c17255bd-8a19-4e31-a960-4235911460fe
  Args:
    source: data:Heinrich_XIII_Prinz_Reuss
    type: :Ancestor
  AssignClass (e2996216-ef96-462b-a459-786efd3d513f)
 Call ID: e2996216-ef96-462b-a459-786efd3d513f
  Args:
    source: data:Adolf_Friedrich_of_Mecklenburg
    type: :Ancestor
  AssignClass (1bb5ba96-4575-4406-ae74-20c8618d9586)
 Call ID: 1bb5ba96-4575-4406-ae74-20c8618d9586
  Args:
    type: :Ancestor
    source: data:Susan_Doukht_Jalali
  AssignClass (ee24a456-d427-4e32-9d2e-d4421e7f04ac)
 Call ID: ee24a456-d427-4e32-9d2e-d4421e7f04ac
  Args:
    type: :Ancestor
    source: data:Henry_II_Count_of_Reuss_Gera
  AssignClass (05fef7aa-b338-43ea-b5d0-04784b50a1c7)
 Call ID: 05fef7aa-b338-43ea-b5d0-04784b50a1c7
  Args:
    source: data:Heinrich_I_Reuss
    type: :Ancestor
  AssignClass (7746dc3f-ba44-4b24-9223-f0bb481e80e2)
 Call ID: 7746dc3f-ba44-4b24-9223-f0bb481e80e2
  Args:
    type: :Ancestor
    source: data:Woizlawa_Feodora_of_Mecklenburg

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Heinrich_XIV_Fuerst_Reuss a :Man .

  data:Vitalia_B a :Woman .

  data:Adolf_Friedrich_of_Mecklenburg a :Ancestor,
          :Man .

  data:Elena a :Woman ;
      :hasFather data:Heinrich_XIII_Prinz_Reuss ;
      :hasMother data:Susan_Doukht_Jalali .

  data:Heinrich_I_Reuss a :Ancestor,
          :Man .

  data:Heinrich_XXVIII a :Man ;
      :hasFather data:Heinrich_XIII_Prinz_Reuss ;
      :hasMother data:Susan_Doukht_Jalali .

  data:Henry_II_Count_of_Reuss_Gera a :Ancestor,
          :Man .

  data:Woizlawa_Feodora_of_Mecklenburg a :Ancestor,
          :Woman ;
      :hasFather data:Adolf_Friedrich_of_Mecklenburg .

  data:Heinrich_XIII_Prinz_Reuss a :Ancestor,
          :Man ;
      :hasAncestor data:Henry_II_Count_of_Reuss_Gera ;
      :hasBirthYear 1951 ;
      :hasDaughter data:Elena ;
      :hasFather data:Heinrich_I_Reuss ;
      :hasMother data:Woizlawa_Feodora_of_Mecklenburg ;
      :hasSon data:Heinrich_XXVIII .

  data:Susan_Doukht_Jalali a :Ancestor,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (393e5123-1c3b-487b-bf4e-3a299dec9984)
 Call ID: 393e5123-1c3b-487b-bf4e-3a299dec9984
  Args:

================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (be0e4ea8-6a5c-4d8b-a1f8-6f90bc309f09)
 Call ID: be0e4ea8-6a5c-4d8b-a1f8-6f90bc309f09
  Args: