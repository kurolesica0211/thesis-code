================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Baroness Gösta von dem Bussche-Haddenhausen (German: Freiin Gösta Julie Adelheid Marion Marie von dem Bussche-Haddenhausen; 26 January 1902 – 13 June 1996) was a German noblewoman and the mother of Prince Claus of the Netherlands.
Life in Germany

Gösta was born at Döbeln, Kingdom of Saxony, German Empire (now Saxony, Germany), the second child and daughter of Baron George von dem Bussche-Haddenhausen (1869–1923), and his wife, Baroness Gabriele von dem Bussche-Ippenburg (1877–1973).
Her father belonged to the Bussche-Haddenhausen branch of the Bussche family, and her mother belonged to the Bussche-Ippenburg branch.
Both of Gösta's parents were descended from Clamor von dem Bussche (1532–1573).
Gösta's mother was the heir of Dötzingen Estate near Hitzacker, which her maternal grandfather had inherited from the Counts von Oeynhausen after 1918.
Gösta's father was an officer in the Royal Saxon Army.
Dötzingen Estate later passed on to Gösta's brother Baron Julius von dem Bussche-Haddenhausen (1906–1977).
After Gösta's return from Africa and her husband's death in 1963, she spent the rest of her life in Dötzingen.
Gösta died at the age of 94 in Hitzacker, Germany.
Marriage

Gösta married Claus Felix von Amsberg (1890–1953), son of Wilhelm von Amsberg and Elise von Vieregge, on 4 September 1924 at Hitzacker.
Together, Gösta and Claus Felix had six daughters and one son:


Life in Africa

Gösta's husband Claus Felix had returned from the Tanganyika Territory (now Tanzania), a German colony, during World War I to become the manager of Dötzingen Estate in 1917.
Shortly after, the estate passed on to the Bussche family.
In 1924, Gösta and Claus Felix married, and in 1926, their son Claus was born at Dötzingen.
Claus Felix was the manager of a German-British tea and sisal plantation.
Claus was sent back to a German boarding school in 1933, but he returned to Africa in 1936.
In 1938, Gösta returned to Germany, and Claus was sent to a boarding school in Misdroy before being drafted by the army.
Gösta's husband returned to Germany in 1947.
Family relations

Gösta was a second cousin of Dorothea von Salviati (wife of Wilhelm, German Crown Prince's eldest son Prince Wilhelm of Prussia), both being great-granddaughters of Heinrich von Salviati and Caroline Rahlenbeck.
Gösta's younger and only brother Julius (1906–1977) was married to Anna-Elisabeth von Pfuel (1909–2005).
Gösta's family's home, Dötzingen Castle in Lower Saxony, had passed to her maternal grandfather, Eberhard Friedrich Gustav von dem Bussche-Ippenburg, from the Counts von Oeynhausen.
At a dinner party hosted by a distant cousin, the Count von Oeynhausen-Sierstorpff in Bad Driburg, on New Year's Eve 1962, Gösta's son Claus met then-Princess Beatrix of the Netherlands for the first time.
Beatrix, like Gösta and Claus, was a cousin of the Counts von Oeynhausen: Beatrix's paternal grandmother Armgard von Cramm was a daughter of Baron Aschwin of Sierstorpff-Cramm (1846–1909) and his wife, Baroness Hedwig von Sierstorpff-Driburg (1848–1900).
Armgard had first been married to Count Bodo von Oeynhausen before marrying Prince Bernhard of Lippe-Biesterfeld (1872–1934), Beatrix's paternal grandfather.
Additionally, Armgard's elder sister Baroness Hedwig von Sierstorpff-Cramm (1874–1907) was the heir to her mother's family's Driburg Estate.
Hedwig also married a Count von Oeynhausen, Wilhelm Karl Ludwig Kuno Graf von Oeynhausen-Sierstorpff (1860–1922), whose descendants still own the Driburg Estate.



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



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (89f44e3c-3348-49f1-bdb1-8ba2035bc347)
 Call ID: 89f44e3c-3348-49f1-bdb1-8ba2035bc347
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    type: :Woman
  AssignClass (ff42ab4a-44e1-474f-89b9-0fed7e6dea74)
 Call ID: ff42ab4a-44e1-474f-89b9-0fed7e6dea74
  Args:
    type: :Man
    source: George_von_dem_Bussche-Haddenhausen
  AssignClass (86a3823e-4eb5-48bc-9e2e-f1654927700f)
 Call ID: 86a3823e-4eb5-48bc-9e2e-f1654927700f
  Args:
    type: :Woman
    source: Gabriele_von_dem_Bussche-Ippenburg
  AssignClass (8cf3692c-302d-40eb-9f1c-787f4f029b5c)
 Call ID: 8cf3692c-302d-40eb-9f1c-787f4f029b5c
  Args:
    type: :Man
    source: Clamor_von_dem_Bussche
  AssignClass (d7ee8b79-fd72-4061-930f-4bf0f1be5079)
 Call ID: d7ee8b79-fd72-4061-930f-4bf0f1be5079
  Args:
    type: :Man
    source: Julius_von_dem_Bussche-Haddenhausen
  AssignClass (cc4be9b6-e1c1-4c1b-b97c-b872a46d7581)
 Call ID: cc4be9b6-e1c1-4c1b-b97c-b872a46d7581
  Args:
    source: Claus_Felix_von_Amsberg
    type: :Man
  AssignClass (8c388bf5-bfc2-4876-9156-382559800a41)
 Call ID: 8c388bf5-bfc2-4876-9156-382559800a41
  Args:
    source: Wilhelm_von_Amsberg
    type: :Man
  AssignClass (fceba95a-57b6-4045-a608-677a42a82db8)
 Call ID: fceba95a-57b6-4045-a608-677a42a82db8
  Args:
    source: Elise_von_Vieregge
    type: :Woman
  AssignClass (b36672ab-2304-4f89-9e59-e5e4984857ba)
 Call ID: b36672ab-2304-4f89-9e59-e5e4984857ba
  Args:
    source: Claus_von_Amsberg
    type: :Man
  AssignClass (9b62abc5-889a-4c48-9c13-7ec27c7cf2e5)
 Call ID: 9b62abc5-889a-4c48-9c13-7ec27c7cf2e5
  Args:
    source: Dorothea_von_Salviati
    type: :Woman
  AssignClass (859cc653-3b9f-4a69-aa5f-a8506b2da7e3)
 Call ID: 859cc653-3b9f-4a69-aa5f-a8506b2da7e3
  Args:
    type: :Man
    source: Heinrich_von_Salviati
  AssignClass (f4c82dde-bf94-47fb-9f88-6e589ac319d9)
 Call ID: f4c82dde-bf94-47fb-9f88-6e589ac319d9
  Args:
    type: :Woman
    source: Caroline_Rahlenbeck
  AssignClass (01b104f1-4c66-4f35-9947-07a44c15b77a)
 Call ID: 01b104f1-4c66-4f35-9947-07a44c15b77a
  Args:
    source: Anna-Elisabeth_von_Pfuel
    type: :Woman
  AssignClass (8b9e4560-f56e-4e10-a9fe-67ff1aeae8e6)
 Call ID: 8b9e4560-f56e-4e10-a9fe-67ff1aeae8e6
  Args:
    type: :Man
    source: Eberhard_Friedrich_Gustav_von_dem_Bussche-Ippenburg
  AssignClass (fc64a5bf-d6d0-49df-af24-6ad4f5eae2cb)
 Call ID: fc64a5bf-d6d0-49df-af24-6ad4f5eae2cb
  Args:
    source: Beatrix_of_the_Netherlands
    type: :Woman
  AssignClass (a725fca4-1cd5-4b4b-ac44-9e115311cd23)
 Call ID: a725fca4-1cd5-4b4b-ac44-9e115311cd23
  Args:
    source: Armgard_von_Cramm
    type: :Woman
  AssignClass (053c045e-23c0-4616-8364-48fc9322e8ec)
 Call ID: 053c045e-23c0-4616-8364-48fc9322e8ec
  Args:
    type: :Man
    source: Aschwin_of_Sierstorpff-Cramm
  AssignClass (4804cebc-92b6-40f1-a6a1-b04984f32759)
 Call ID: 4804cebc-92b6-40f1-a6a1-b04984f32759
  Args:
    source: Hedwig_von_Sierstorpff-Driburg
    type: :Woman
  AssignClass (28a1e48c-6b12-4673-aded-81068ee0188f)
 Call ID: 28a1e48c-6b12-4673-aded-81068ee0188f
  Args:
    type: :Man
    source: Bodo_von_Oeynhausen
  AssignClass (f1a77584-305f-4af6-bc6a-a142b27f83df)
 Call ID: f1a77584-305f-4af6-bc6a-a142b27f83df
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (8d9d7819-ee2b-44a0-93e0-77d3c2eb689f)
 Call ID: 8d9d7819-ee2b-44a0-93e0-77d3c2eb689f
  Args:
    source: Hedwig_von_Sierstorpff-Cramm
    type: :Woman
  AssignClass (941f8334-44f6-44ea-8233-24058aaf6a41)
 Call ID: 941f8334-44f6-44ea-8233-24058aaf6a41
  Args:
    type: :Man
    source: Wilhelm_Karl_Ludwig_Kuno_Graf_von_Oeynhausen-Sierstorpff
  AddLiteral (25ff544f-6430-4032-9100-a1aceef5aaaa)
 Call ID: 25ff544f-6430-4032-9100-a1aceef5aaaa
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1902
    source: Gösta_von_dem_Bussche-Haddenhausen
  AddLiteral (1f895e07-a313-4a6f-a5cd-ff9febec4452)
 Call ID: 1f895e07-a313-4a6f-a5cd-ff9febec4452
  Args:
    relation: :hasDeathYear
    literal_value: 1996
    literal_type: xsd:integer
    source: Gösta_von_dem_Bussche-Haddenhausen
  AddTriple (c3fd99f3-996f-4544-9ebf-472923729c30)
 Call ID: c3fd99f3-996f-4544-9ebf-472923729c30
  Args:
    target: George_von_dem_Bussche-Haddenhausen
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasFather
  AddTriple (499af370-2994-4c51-92dc-ba4a42b662ff)
 Call ID: 499af370-2994-4c51-92dc-ba4a42b662ff
  Args:
    source: Gösta_von_dem_Bussche-Haddenhausen
    target: Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasMother
  AddLiteral (7adcb3d0-5c58-45bd-8870-40a4e9161d24)
 Call ID: 7adcb3d0-5c58-45bd-8870-40a4e9161d24
  Args:
    literal_type: xsd:integer
    literal_value: 1869
    source: George_von_dem_Bussche-Haddenhausen
    relation: :hasBirthYear
  AddLiteral (90b2e0fa-8f3a-46db-9f5d-bf50109e9a63)
 Call ID: 90b2e0fa-8f3a-46db-9f5d-bf50109e9a63
  Args:
    source: George_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    literal_value: 1923
    relation: :hasDeathYear
  AddLiteral (4f709bca-f7c7-4a68-8d2d-c2f0d15b4785)
 Call ID: 4f709bca-f7c7-4a68-8d2d-c2f0d15b4785
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_value: 1877
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (da6bbf8e-8bb1-4c86-8934-7e109d258495)
 Call ID: da6bbf8e-8bb1-4c86-8934-7e109d258495
  Args:
    literal_type: xsd:integer
    literal_value: 1973
    source: Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasDeathYear
  AddTriple (8220f0f2-80e4-4fb0-ab65-2f4610306d62)
 Call ID: 8220f0f2-80e4-4fb0-ab65-2f4610306d62
  Args:
    source: Clamor_von_dem_Bussche
    target: George_von_dem_Bussche-Haddenhausen
    relation: :isAncestorOf
  AddTriple (851fa7aa-6768-454b-8ded-e2e0020a0048)
 Call ID: 851fa7aa-6768-454b-8ded-e2e0020a0048
  Args:
    relation: :isAncestorOf
    source: Clamor_von_dem_Bussche
    target: Gabriele_von_dem_Bussche-Ippenburg
  AddTriple (7fe79e36-68cd-4237-bbec-45339ce9c28c)
 Call ID: 7fe79e36-68cd-4237-bbec-45339ce9c28c
  Args:
    target: Julius_von_dem_Bussche-Haddenhausen
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasBrother
  AddLiteral (1aa5526a-3db4-49bd-9c9a-e80172a88bac)
 Call ID: 1aa5526a-3db4-49bd-9c9a-e80172a88bac
  Args:
    literal_type: xsd:integer
    literal_value: 1906
    source: Julius_von_dem_Bussche-Haddenhausen
    relation: :hasBirthYear
  AddLiteral (ff9ed94d-c72a-46cc-8474-5655e266737b)
 Call ID: ff9ed94d-c72a-46cc-8474-5655e266737b
  Args:
    relation: :hasDeathYear
    literal_value: 1977
    literal_type: xsd:integer
    source: Julius_von_dem_Bussche-Haddenhausen
  AddTriple (75b6a18c-6d0a-4c0f-ac3e-89d9cea133d6)
 Call ID: 75b6a18c-6d0a-4c0f-ac3e-89d9cea133d6
  Args:
    relation: :hasFather
    target: Claus_Felix_von_Amsberg
    source: Claus_von_Amsberg
  AddTriple (bf4cecb6-bbfa-4859-b369-4fd6e30a8bb5)
 Call ID: bf4cecb6-bbfa-4859-b369-4fd6e30a8bb5
  Args:
    target: Gösta_von_dem_Bussche-Haddenhausen
    source: Claus_von_Amsberg
    relation: :hasMother
  AddTriple (9dfff7f7-f66e-42a4-9289-61d0adef66a6)
 Call ID: 9dfff7f7-f66e-42a4-9289-61d0adef66a6
  Args:
    relation: :hasFather
    source: Claus_Felix_von_Amsberg
    target: Wilhelm_von_Amsberg
  AddTriple (e5de87fb-de21-4760-8f92-4498c29bcca0)
 Call ID: e5de87fb-de21-4760-8f92-4498c29bcca0
  Args:
    relation: :hasMother
    target: Elise_von_Vieregge
    source: Claus_Felix_von_Amsberg
  AddLiteral (85f808d1-c2b0-4fb9-aca8-16dd32c3dec8)
 Call ID: 85f808d1-c2b0-4fb9-aca8-16dd32c3dec8
  Args:
    literal_type: xsd:integer
    literal_value: 1924
    source: Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasMarriageYear
  AddTriple (d9936eb5-0ba6-4ebc-88de-ab9c37e2f804)
 Call ID: d9936eb5-0ba6-4ebc-88de-ab9c37e2f804
  Args:
    target: Caroline_Rahlenbeck
    source: Dorothea_von_Salviati
    relation: :hasMother
  AddTriple (09d21c0d-ed64-492a-a3df-8910795701e6)
 Call ID: 09d21c0d-ed64-492a-a3df-8910795701e6
  Args:
    relation: :hasFather
    target: Heinrich_von_Salviati
    source: Dorothea_von_Salviati
  AddTriple (1ce048cb-23bd-4dcf-b70d-90d2a3fe601b)
 Call ID: 1ce048cb-23bd-4dcf-b70d-90d2a3fe601b
  Args:
    target: Eberhard_Friedrich_Gustav_von_dem_Bussche-Ippenburg
    source: Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasMother
  AddTriple (d3ceda84-a5ec-45d0-b461-8c53f894deaf)
 Call ID: d3ceda84-a5ec-45d0-b461-8c53f894deaf
  Args:
    source: Armgard_von_Cramm
    target: Aschwin_of_Sierstorpff-Cramm
    relation: :hasFather
  AddTriple (175322cf-f021-4c10-8ea6-5fcf8883a529)
 Call ID: 175322cf-f021-4c10-8ea6-5fcf8883a529
  Args:
    target: Hedwig_von_Sierstorpff-Driburg
    source: Armgard_von_Cramm
    relation: :hasMother
  AddTriple (0def4cca-7022-4f4a-b4d3-4761e6352471)
 Call ID: 0def4cca-7022-4f4a-b4d3-4761e6352471
  Args:
    relation: :hasMother
    source: Hedwig_von_Sierstorpff-Cramm
    target: Hedwig_von_Sierstorpff-Driburg
  AddTriple (8298114c-611c-4997-8b8f-6f288e7781f0)
 Call ID: 8298114c-611c-4997-8b8f-6f288e7781f0
  Args:
    source: Hedwig_von_Sierstorpff-Cramm
    target: Aschwin_of_Sierstorpff-Cramm
    relation: :hasFather
  Finish (70048a31-3578-4f8b-bdc4-57e219e49d61)
 Call ID: 70048a31-3578-4f8b-bdc4-57e219e49d61
  Args: