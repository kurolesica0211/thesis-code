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
Ernst August, Hereditary Prince of Hanover (German:
Ernst August Prinz von Hannover Herzog zu Braunschweig und Lüneburg, Königlicher Prinz von Großbritannien und Irland; born 19 July 1983) is a German financier and the eldest child of Ernst August, Prince of Hanover (head of the ancient House of Hanover which once ruled the Kingdom of Hanover and were rulers of Great Britain until 1901) and his first wife Chantal Hochuli.
Due to his father's second marriage, he is also the stepson of Caroline, Princess of Hanover, a Monegasque Princess and the sister of Albert II of Monaco.
Background

Ernst August and his younger brother Christian were born in Hildesheim, Lower Saxony, while their half-sister, Alexandra, was born in Austria and lives with her mother in Monaco.
Ernst August was baptized on 15 October 1983 at Marienburg Castle, his godparents including Felipe VI of Spain and Constantine II of Greece.
Until his mid-teens, Ernst August and his brother lived at Hurlingham Lodge in London.
He also descends from Germany's last emperor, Wilhelm II, following whose abdication at the end of World War I the Hanovers also lost sovereignty over the Duchy of Brunswick, while retaining much of their continental personal property.
Education

Ernst August began his secondary education at Malvern College, but ultimately completed that phase of his education with an International Baccalaureate back on the Continent.
After his marriage in 2017 he and his wife moved to Hanover.
Already in 2004, his father had signed over to him the German property of the House of Hanover, including gothic-revival Marienburg Castle, the agricultural estates of Calenberg Castle and the Fürstenhaus ("Princely House") at Herrenhausen Gardens in Hanover; the elaborate museum in this small palace, built by King George I of Great Britain in 1720, has been closed to the public since 2011.
Since 2004, the prince has taken over many representative tasks on behalf of his father.
The father remained in charge of the Austrian family assets until 2013 when he was removed from the chairmanship of a family foundation based in Liechtenstein, the Duke of Cumberland Foundation, which holds the properties near Gmunden in Austria, the Hanovers' main residence in exile after 1866 when their Kingdom of Hanover was annexed by Prussia.
Instead, the younger Ernst August was put in charge, reportedly for negligence on part of his father, at the initiative of the foundation's trustee Prince Michael of Liechtenstein.
In 2017 Ernst August the Elder filed legal action to recover chairmanship.
In 2014, Ernst August lent a number of paintings and objects for a Lower Saxony state exhibition, When the Royals came from Hanover - The rulers of Hanover on England's throne, which included exhibits in five museums and castles under the auspices of Charles, Prince of Wales.
Thirty of more than 1000 items were contributed by Elizabeth II, including the State Crown of George I, while Ernst August provided the king's famous Augsburg silver throne and other furniture dating to 1720.
He hosted a parallel exhibition, The Way to the Crown, at Marienburg Castle until through 2016, displaying—among other items—the crown jewels of the Kingdom of Hanover.
Marriage and issue

In the summer of 2016 Ernst August became engaged to Ekaterina Igorievna Malysheva (born 30 July 1986, Apatity, Soviet Russia), a Russian designer, general manager of Audiotube and founder of EKAT, and daughter of Igor Malyshev and Svetlana Malysheva.
Days before the wedding, his father, the elder Ernst August publicly stated concerns about potential adverse impacts on family assets if the younger Ernst August were to marry his chosen fiancée.
Despite the dynastic tradition of obtaining the head of the House of Hanover's express, prior authorization for an heir's marriage in accordance with an 1836 Hanoverian house law (as Ernst August's father had done when marrying his sons' future mother in 1981), the bridegroom's father declared his intention to withhold consent for his son's marriage to Ekaterina Malysheva, reportedly in a dispute over family assets.
Nonetheless, the civil marriage took place on 6 July 2017 in Hanover's New Town Hall and was conducted by the mayor of Hanover, Stefan Schostok.
The church marriage took place on 8 July 2017 in the Hanover Market Church at which the former Landesbischof of the Evangelical-Lutheran Church of Hanover, Horst Hirschler, presided.
Her wedding dress was the work of Lebanese designer Sandra Mansour, and she wore a tiara that belonged to the former Kaiser Wilhelm II's only daughter, Princess Victoria Louise of Prussia.
Among the wedding guests were: Prince Christian of Hanover, Princess Alexandra of Hanover, Andrea Casiraghi, Tatiana Santo Domingo, Pierre Casiraghi, Beatrice Borromeo, Charlotte Casiraghi, Georg Friedrich, Prince of Prussia and his wife Princess Sophie, Crown Prince Pavlos of Greece and his wife Crown Princess Marie-Chantal, Hereditary Prince Hubertus of Saxe-Coburg and Gotha, Alexander, Prince of Schaumburg-Lippe and Princess Elisabeth von Thurn und Taxis.
The father of the groom, Prince Ernst August, did not attend the wedding.
Thus, while descendants of non-dynastic marriages may have a legal right to the use of "Prinz/Prinzessin von Hannover Herzog/Herzogin zu Braunschweig und Lüneburg Königlicher Prinz/Prinzessin von Großbritannien und Irland" as surnames, they are not recognized as bearing rank, styles titles or membership appertaining to the House of Hanover, according to its house rules.
Nor is the title "Prince/ss of Great Britain and Ireland", re-claimed by the deposed House of Hanover in 1931, accorded by British sovereigns to members thereof born after 30 November 1917.


Notes and references

External links



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (72180269-f64d-4fb4-867b-76f092c4a65e)
 Call ID: 72180269-f64d-4fb4-867b-76f092c4a65e
  Args:
    source: :Ernst_August_Hereditary_Prince_of_Hanover
    type: :Man
  AssignClass (5811f834-1d6b-48a7-afe2-20c6a3465d74)
 Call ID: 5811f834-1d6b-48a7-afe2-20c6a3465d74
  Args:
    source: :Ernst_August_Prince_of_Hanover
    type: :Man
  AssignClass (16602d28-440c-4761-bde3-8585366c3f36)
 Call ID: 16602d28-440c-4761-bde3-8585366c3f36
  Args:
    type: :Woman
    source: :Chantal_Hochuli
  AssignClass (e227267a-6c73-4b7a-ab4f-6e8774f877c2)
 Call ID: e227267a-6c73-4b7a-ab4f-6e8774f877c2
  Args:
    source: :Christian_of_Hanover
    type: :Man
  AssignClass (798d8c1c-08fc-47aa-bc36-bc896441eb7e)
 Call ID: 798d8c1c-08fc-47aa-bc36-bc896441eb7e
  Args:
    source: :Alexandra_of_Hanover
    type: :Woman
  AssignClass (6ab0df6c-e926-4709-bac6-6af97e65ed4c)
 Call ID: 6ab0df6c-e926-4709-bac6-6af97e65ed4c
  Args:
    type: :Woman
    source: :Ekaterina_Igorievna_Malysheva
  AssignClass (11558d00-8931-4dec-8c6b-3495c956fdc2)
 Call ID: 11558d00-8931-4dec-8c6b-3495c956fdc2
  Args:
    source: :Igor_Malyshev
    type: :Man
  AssignClass (5cc9f248-3e52-4cf7-9ccf-597be84e33f3)
 Call ID: 5cc9f248-3e52-4cf7-9ccf-597be84e33f3
  Args:
    type: :Woman
    source: :Svetlana_Malysheva
  AddLiteral (224620df-f582-414d-97cd-c993785c241f)
 Call ID: 224620df-f582-414d-97cd-c993785c241f
  Args:
    literal_type: xsd:integer
    source: :Ernst_August_Hereditary_Prince_of_Hanover
    literal_value: 1983
    relation: :hasBirthYear
  AddTriple (aa302264-a019-4314-9431-fd9aff3408e5)
 Call ID: aa302264-a019-4314-9431-fd9aff3408e5
  Args:
    source: :Ernst_August_Hereditary_Prince_of_Hanover
    target: :Ernst_August_Prince_of_Hanover
    relation: :hasFather
  AddTriple (f5ef247d-47d1-4c80-97ac-967d76ee7f55)
 Call ID: f5ef247d-47d1-4c80-97ac-967d76ee7f55
  Args:
    relation: :hasMother
    source: :Ernst_August_Hereditary_Prince_of_Hanover
    target: :Chantal_Hochuli
  AddTriple (e4624167-9e94-409e-b106-8c38e2a076fb)
 Call ID: e4624167-9e94-409e-b106-8c38e2a076fb
  Args:
    relation: :isBrotherOf
    source: :Christian_of_Hanover
    target: :Ernst_August_Hereditary_Prince_of_Hanover
  AddTriple (395c4d1a-305e-44d9-979a-03bafd8cb69a)
 Call ID: 395c4d1a-305e-44d9-979a-03bafd8cb69a
  Args:
    relation: :hasFather
    target: :Ernst_August_Prince_of_Hanover
    source: :Christian_of_Hanover
  AddTriple (2dcdfa39-c5bf-4aca-9666-4b8ac11412d9)
 Call ID: 2dcdfa39-c5bf-4aca-9666-4b8ac11412d9
  Args:
    source: :Christian_of_Hanover
    target: :Chantal_Hochuli
    relation: :hasMother
  AddTriple (71faacd9-4f16-4a75-ba7e-e7eb9c128178)
 Call ID: 71faacd9-4f16-4a75-ba7e-e7eb9c128178
  Args:
    source: :Alexandra_of_Hanover
    target: :Ernst_August_Prince_of_Hanover
    relation: :hasFather
  AddLiteral (a38b577b-56c5-49c7-88a0-741e6ae5cc49)
 Call ID: a38b577b-56c5-49c7-88a0-741e6ae5cc49
  Args:
    literal_type: xsd:integer
    source: :Ekaterina_Igorievna_Malysheva
    literal_value: 1986
    relation: :hasBirthYear
  AddTriple (a4a4b8c0-0ba7-45f2-8648-14c48765ac05)
 Call ID: a4a4b8c0-0ba7-45f2-8648-14c48765ac05
  Args:
    source: :Ekaterina_Igorievna_Malysheva
    target: :Igor_Malyshev
    relation: :hasFather
  AddTriple (2ec4c7d0-7d34-4c89-a78f-b5332a0b6681)
 Call ID: 2ec4c7d0-7d34-4c89-a78f-b5332a0b6681
  Args:
    source: :Ekaterina_Igorievna_Malysheva
    target: :Svetlana_Malysheva
    relation: :hasMother
  AddLiteral (3b9c1a95-d2fa-4a90-9902-c8f8b94445a6)
 Call ID: 3b9c1a95-d2fa-4a90-9902-c8f8b94445a6
  Args:
    literal_value: 2017
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Ernst_August_Hereditary_Prince_of_Hanover
  Finish (16fc0914-47a3-4a1a-a0d2-939da91fed8f)
 Call ID: 16fc0914-47a3-4a1a-a0d2-939da91fed8f
  Args: