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
Prince Christopher of Greece and Denmark (Greek: Χριστόφορος, romanized: Christóphoros; 10 August 1888 – 21 January 1940) was the fifth and youngest son and youngest child of King George I of Greece, belonging to a dynasty which mounted and lost the throne of Greece several times during his lifetime.
Family background

Christopher was born at Pavlovsk, Imperial Russia, son of King George I of Greece and Queen Olga, a Russian grand duchess by birth.
He was called "Christo" in the family.
His older brothers were future King Constantine I, George, Nicholas and Andrew.
Christopher, like his siblings, was a polyglot, speaking Greek, English, Danish, Russian, French, and Italian.
The Hellenic royal line was a cadet branch of the Schleswig-Holstein-Sonderburg-Glücksburg dynasty which had mounted the throne of Greece in 1863.
Early adulthood

When Christopher came of age he joined the Hellenic Navy, although apparently he would rather have studied the piano.
He was briefly engaged to Princess Alexandra, 2nd Duchess of Fife in about 1910 (Alexandra's mother, Princess Louise, Duchess of Fife, was a daughter of King Edward VII and Queen Alexandra of the United Kingdom, herself an older sister of George I of Greece, Christopher's father).
First marriage

On 1 January 1920, Christopher married a very wealthy American widow, Nonnie May "Nancy" Stewart Worthington Leeds, at Vevey, Switzerland.
His bride, a once-divorced and once-widowed commoner at least a decade older than the prince, was nonetheless recognised as Christopher's dynastic wife by his family (at the time of the engagement and wedding, the Greek royal family lived frugally in exile, and as Christopher was last in the dynasty's order of succession, any children he fathered would not impact the succession rights of other Greek dynasts).
Shortly after their marriage, Princess Anastasia developed cancer, and died in London on 29 August 1923, leaving no children from this marriage.
Prince Christopher did, however, have a stepson, William Bateman Leeds Jr (1902–1971), who had, in 1921, married Princess Xenia Georgievna of Russia.
She was Christopher's niece through his elder sister, Marie of Greece, Grand Duchess George of Russia.
Second marriage and family

Prince Christopher later remarried; his second wife was Princess Françoise of Orléans (25 December 1902 – 25 February 1953).
Françoise was a daughter of Jean d'Orléans, Duc de Guise, Orléanist pretender to the throne of France, by his wife/first cousin, Isabelle d'Orléans.
Isabelle was, in turn, a daughter of Philippe, Comte de Paris by his wife and first cousin, Infanta Isabel de Orléans y Borbon.
They were childless for a decade, then one child was born to Françoise: Prince Michael of Greece and Denmark was born in Rome in 1939, shortly before Prince Christopher's death.
Opinion on Anna Anderson

In 1927, Prince Christopher paid a visit to the Long Island home of William and Xenia Leeds, respectively his stepson and niece.
Xenia had taken an interest in the strange case of a woman, Anna Anderson, who claimed to be Grand Duchess Anastasia Nikolaevna of Russia, the youngest daughter of the last Tsar of Russia, Nicholas II.
As Prince Christopher explained, "That was her story, and, fantastic as it was, there were many who believed then − and still believe − in her, among them one or two members of the Imperial Family."
Prince Christopher described her: "In the first place she was unable to speak Russian, which the Grand Duchess Anastasia, like all the Czar's children, had talked fluently − and would only converse in German.
Opinion on monarchy

Prince Christopher recorded his thoughts on monarchy and those aspiring to it: "Nothing under the sun would induce me to accept a Kingdom.
"


Death

Prince Christopher of Greece died in Athens on 21 January 1940, aged 51.



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
  AssignClass (86c755d3-605f-4b98-a786-a17311729d03)
 Call ID: 86c755d3-605f-4b98-a786-a17311729d03
  Args:
    type: :Man
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (44887bae-e538-4ef5-9f18-b982a16473fa)
 Call ID: 44887bae-e538-4ef5-9f18-b982a16473fa
  Args:
    type: :Person
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (269dd0be-92da-4237-be5f-4615b800deda)
 Call ID: 269dd0be-92da-4237-be5f-4615b800deda
  Args:
    source: King_George_I_of_Greece
    type: :Man
  AssignClass (79ccef41-50a0-47d5-825d-faac692c244e)
 Call ID: 79ccef41-50a0-47d5-825d-faac692c244e
  Args:
    type: :Person
    source: King_George_I_of_Greece
  AssignClass (e768b341-11ea-431e-9c39-dfdfbfd9264e)
 Call ID: e768b341-11ea-431e-9c39-dfdfbfd9264e
  Args:
    type: :Woman
    source: Queen_Olga_of_Greece
  AssignClass (63c57ecd-5ecc-42e7-8676-35d576b8abd0)
 Call ID: 63c57ecd-5ecc-42e7-8676-35d576b8abd0
  Args:
    source: Queen_Olga_of_Greece
    type: :Person
  AddLiteral (c5148c12-b866-42fb-b53d-4f0818e3f59b)
 Call ID: c5148c12-b866-42fb-b53d-4f0818e3f59b
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    literal_value: 1888
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (143cd876-6493-4dbe-ac12-c7c32db5b91c)
 Call ID: 143cd876-6493-4dbe-ac12-c7c32db5b91c
  Args:
    literal_value: 1940
    literal_type: xsd:integer
    source: Prince_Christopher_of_Greece_and_Denmark
    relation: :hasDeathYear
  AddTriple (6163086a-ebaa-4a2e-99eb-b8f5107ba284)
 Call ID: 6163086a-ebaa-4a2e-99eb-b8f5107ba284
  Args:
    relation: :hasFather
    target: King_George_I_of_Greece
    source: Prince_Christopher_of_Greece_and_Denmark
  AddTriple (030bb06b-d03f-4ff1-a770-69d0834e3886)
 Call ID: 030bb06b-d03f-4ff1-a770-69d0834e3886
  Args:
    target: Queen_Olga_of_Greece
    source: Prince_Christopher_of_Greece_and_Denmark
    relation: :hasMother
  AddLiteral (99bd78a3-243d-48bd-88da-c8b58a518e7b)
 Call ID: 99bd78a3-243d-48bd-88da-c8b58a518e7b
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    literal_type: xsd:string
    literal_value: Christo
    relation: :knownAs
  AssignClass (1e06db2a-0567-40f5-a80f-598d4610cb13)
 Call ID: 1e06db2a-0567-40f5-a80f-598d4610cb13
  Args:
    source: Constantine_I_of_Greece
    type: :Man
  AssignClass (a438bc31-6b75-4f1b-88af-1374fee80545)
 Call ID: a438bc31-6b75-4f1b-88af-1374fee80545
  Args:
    source: Constantine_I_of_Greece
    type: :Person
  AssignClass (6c882bd4-33a1-429c-b85a-c935c4ce15e4)
 Call ID: 6c882bd4-33a1-429c-b85a-c935c4ce15e4
  Args:
    source: George_of_Greece
    type: :Man
  AssignClass (d2566b1c-e77e-4d1d-955a-11c4b31646db)
 Call ID: d2566b1c-e77e-4d1d-955a-11c4b31646db
  Args:
    source: George_of_Greece
    type: :Person
  AssignClass (aacade66-e8da-4530-ab83-2f99758d0866)
 Call ID: aacade66-e8da-4530-ab83-2f99758d0866
  Args:
    source: Nicholas_of_Greece
    type: :Man
  AssignClass (dfbf0f15-0f03-4a5e-a3f8-04a0ea49ddde)
 Call ID: dfbf0f15-0f03-4a5e-a3f8-04a0ea49ddde
  Args:
    type: :Person
    source: Nicholas_of_Greece
  AssignClass (76cd4014-cec0-41ff-90f8-69f21375ad40)
 Call ID: 76cd4014-cec0-41ff-90f8-69f21375ad40
  Args:
    type: :Man
    source: Andrew_of_Greece
  AssignClass (00af3f3d-423b-4291-9b2f-15ed218ba356)
 Call ID: 00af3f3d-423b-4291-9b2f-15ed218ba356
  Args:
    type: :Person
    source: Andrew_of_Greece
  AddTriple (62238878-bcd0-41d2-ac32-340d54ad90d4)
 Call ID: 62238878-bcd0-41d2-ac32-340d54ad90d4
  Args:
    relation: :isBrotherOf
    source: Constantine_I_of_Greece
    target: Prince_Christopher_of_Greece_and_Denmark
  AddTriple (a4579333-3f4b-435a-af1c-d5d6e33367fe)
 Call ID: a4579333-3f4b-435a-af1c-d5d6e33367fe
  Args:
    source: George_of_Greece
    target: Prince_Christopher_of_Greece_and_Denmark
    relation: :isBrotherOf
  AddTriple (1df30c11-2935-4674-9f12-b79789c885cb)
 Call ID: 1df30c11-2935-4674-9f12-b79789c885cb
  Args:
    relation: :isBrotherOf
    source: Nicholas_of_Greece
    target: Prince_Christopher_of_Greece_and_Denmark
  AddTriple (5363947d-bd06-43df-84c3-69f7c29506b5)
 Call ID: 5363947d-bd06-43df-84c3-69f7c29506b5
  Args:
    relation: :isBrotherOf
    source: Andrew_of_Greece
    target: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (655806fd-40bd-4cac-bcf8-ac96942e6eb9)
 Call ID: 655806fd-40bd-4cac-bcf8-ac96942e6eb9
  Args:
    type: :Woman
    source: Nonnie_May_Stewart_Worthington_Leeds
  AssignClass (26a9f736-2f85-49f9-9ebf-9b2007e739a8)
 Call ID: 26a9f736-2f85-49f9-9ebf-9b2007e739a8
  Args:
    type: :Person
    source: Nonnie_May_Stewart_Worthington_Leeds
  AddLiteral (a1ef0a72-23ec-4b89-9913-999e9537a7e6)
 Call ID: a1ef0a72-23ec-4b89-9913-999e9537a7e6
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    literal_value: 1920
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddLiteral (731edb10-46c5-4cc1-b823-deba7501ce92)
 Call ID: 731edb10-46c5-4cc1-b823-deba7501ce92
  Args:
    source: Nonnie_May_Stewart_Worthington_Leeds
    literal_value: 1923
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (59294fdd-4b35-4767-94ab-e71be692101e)
 Call ID: 59294fdd-4b35-4767-94ab-e71be692101e
  Args:
    type: :Man
    source: William_Bateman_Leeds_Jr
  AssignClass (c71b5e5e-3b04-497b-bd51-46af938bf99c)
 Call ID: c71b5e5e-3b04-497b-bd51-46af938bf99c
  Args:
    source: William_Bateman_Leeds_Jr
    type: :Person
  AddTriple (0b6502ba-6298-4b5b-a470-2049136f12c2)
 Call ID: 0b6502ba-6298-4b5b-a470-2049136f12c2
  Args:
    relation: :hasRelation
    target: William_Bateman_Leeds_Jr
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (1d896263-ff08-424b-95c4-a8c9ffe74811)
 Call ID: 1d896263-ff08-424b-95c4-a8c9ffe74811
  Args:
    source: Princess_Xenia_Georgievna_of_Russia
    type: :Woman
  AssignClass (78bc28e5-8af4-49b4-b36e-cbfd1159905a)
 Call ID: 78bc28e5-8af4-49b4-b36e-cbfd1159905a
  Args:
    type: :Person
    source: Princess_Xenia_Georgievna_of_Russia
  AssignClass (ead1e54e-68c7-4de6-ab47-93b2491d8ba4)
 Call ID: ead1e54e-68c7-4de6-ab47-93b2491d8ba4
  Args:
    type: :Woman
    source: Marie_of_Greece
  AssignClass (cca755d9-7853-479a-ada0-affd6e1cc23d)
 Call ID: cca755d9-7853-479a-ada0-affd6e1cc23d
  Args:
    source: Marie_of_Greece
    type: :Person
  AddTriple (69c93854-2f67-4672-badd-f3448f0792f8)
 Call ID: 69c93854-2f67-4672-badd-f3448f0792f8
  Args:
    target: Prince_Christopher_of_Greece_and_Denmark
    source: Marie_of_Greece
    relation: :isSisterOf
  AssignClass (8838431c-63f8-478a-b0bd-a1b46c6156c2)
 Call ID: 8838431c-63f8-478a-b0bd-a1b46c6156c2
  Args:
    source: Princess_Francoise_of_Orleans
    type: :Woman
  AssignClass (d0b6c9cc-36b2-4a0d-ac78-03daab16c76b)
 Call ID: d0b6c9cc-36b2-4a0d-ac78-03daab16c76b
  Args:
    source: Princess_Francoise_of_Orleans
    type: :Person
  AddLiteral (ac56eef0-ee46-4e81-8831-ad619994e05c)
 Call ID: ac56eef0-ee46-4e81-8831-ad619994e05c
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1939
    relation: :hasBirthYear
  AssignClass (144dff86-f94e-427e-b1a0-4d4684d6033e)
 Call ID: 144dff86-f94e-427e-b1a0-4d4684d6033e
  Args:
    type: :Man
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (88433727-f4c2-413c-b214-641800d39fb0)
 Call ID: 88433727-f4c2-413c-b214-641800d39fb0
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AddTriple (f08748a7-c1c7-4610-81d1-2a52d6a62c70)
 Call ID: f08748a7-c1c7-4610-81d1-2a52d6a62c70
  Args:
    source: Prince_Christopher_of_Greece_and_Denmark
    target: Prince_Michael_of_Greece_and_Denmark
    relation: :isFatherOf
  AddTriple (97a651d3-567d-4f86-b69f-9843d9749bc8)
 Call ID: 97a651d3-567d-4f86-b69f-9843d9749bc8
  Args:
    relation: :isMotherOf
    source: Princess_Francoise_of_Orleans
    target: Prince_Michael_of_Greece_and_Denmark
  Finish (4c3cfe8b-060a-4d4c-9f37-cce38dcbe357)
 Call ID: 4c3cfe8b-060a-4d4c-9f37-cce38dcbe357
  Args: