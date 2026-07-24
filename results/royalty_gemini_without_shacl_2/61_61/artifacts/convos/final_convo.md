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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Willem-Alexander (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Dutch: ; Willem-Alexander Claus George Ferdinand; born 27 April 1967) is the current King of the Netherlands, having reigned since 30 April 2013.
Willem-Alexander was born in Utrecht during the reign of his maternal grandmother, Queen Juliana, as the eldest child of Princess Beatrix (later Queen) and Prince Claus.
He went to public primary and secondary schools in the Netherlands, and an international sixth-form college in Wales.
He served in the Royal Netherlands Navy, and studied history at Leiden University.
He married Máxima Zorreguieta Cerruti in 2002, and they have three daughters: Catharina-Amalia, Alexia, and Ariane.
He is the first man to hold this position since the death of his great-great-grandfather William III in 1890, as the intervening three monarchs—his great-grandmother Wilhelmina, his grandmother Juliana and his mother Beatrix—had all been women.
He is the first child of Princess Beatrix (later Queen) and Prince Claus, and the first grandchild of Queen Juliana and Prince Bernhard.
From birth, Willem-Alexander has held the titles Prince of the Netherlands (Dutch: Prins der Nederlanden), Prince of Orange-Nassau, and Jonkheer of Amsberg.
His godparents are his maternal grandfather Prince Bernhard of Lippe-Biesterfeld, his paternal grandmother Gösta Freiin von dem Bussche-Haddenhausen, Prince Ferdinand von Bismarck, former Prime Minister Jelle Zijlstra, Jonkvrouw Renée Röell, and Queen Margrethe II.
He had two younger brothers: Prince Friso (1968–2013) and Prince Constantijn (b. 1969).
His mother, Beatrix, became Queen of the Netherlands in 1980, after his grandmother Juliana abdicated.
He then received the title of Prince of Orange as heir apparent to the throne of the Kingdom of the Netherlands at the age of 13.
Military training and career

Between secondary school and his university education, Willem-Alexander performed military service in the Royal Netherlands Navy from August 1985 until January 1987.
He received his training at the Royal Netherlands Naval College and in the frigates HNLMS Tromp and HNLMS Abraham Crijnssen, where he was an ensign.
As a reservist for the Royal Netherlands Navy, Willem-Alexander was promoted to lieutenant commander in 1995, commander in 1997, Captain at Sea in 2001, and commodore in 2005.
As a reservist for the Royal Netherlands Army, he was made a major (Grenadiers' and Rifles Guard Regiment) in 1995, and was promoted to lieutenant colonel in 1997, colonel in 2001, and brigadier general in 2005.
As a reservist for the Royal Netherlands Air Force, he was made squadron leader in 1995 and promoted to air commodore in 2005.
Activities and social interests

Since 1985, when he became 18 years old, Willem-Alexander has been a member of the Council of State of the Netherlands.
This is the highest council of the Dutch political system and is chaired by the head of state (then Queen Beatrix).
On 10 October 2010, Willem-Alexander and Máxima went to the Netherlands Antilles' capital, Willemstad, to attend and represent his mother, the Queen, at the Antillean Dissolution ceremony.
Reign

On 28 January 2013, Beatrix announced her intention to abdicate.
On the morning of 30 April 2013 (Koninginnedag), Beatrix signed the instrument of abdication at the Moseszaal (Moses Hall) at the Royal Palace of Amsterdam.
He is also the first male monarch of the Netherlands since the death of his great-great-grandfather William III in 1890.
Using the name "W. A. van Buren", one of the least-known titles of the House of Orange-Nassau, he completed the 1986 Frisian Elfstedentocht, a 200-kilometre-long (120 mi) distance ice skating tour.
Marriage and children

On 2 February 2002, he married Máxima Zorreguieta at the Nieuwe Kerk in Amsterdam.
Privacy and the press

In an attempt to strike a balance between privacy for the royal family and availability to the press, the Netherlands Government Information Service (RVD) instituted a media code on 21 June 2005 which essentially states that:


During a ski vacation in Argentina, several photographs were taken of the prince and his family during the private part of their holiday, including one by Associated Press staff photographer Natacha Pisarenko, in spite of the media code, and after a photo opportunity had been provided earlier.
Willem-Alexander and the RVD jointly filed suit against the Associated Press on 5 August 2009, and the trial started on 14 August 2009 at the district court in Amsterdam.
On 28 August 2009, the district court ruled in favour of the prince and RVD, citing that the couple has a right to privacy, that the pictures in question add nothing to any public debate, and that they are not of any particular value to society since they are not photographs of his family "at work".
In October 2020, Willem-Alexander apologised for a family holiday trip to Greece which had taken place while his country was under partial lockdown during the COVID-19 pandemic.
Properties

From 2003 until 2019, Willem-Alexander and his family lived in Villa Eikenhorst on the De Horsten Estate in Wassenaar.
After his mother abdicated and became Princess Beatrix once again, she moved to the castle of Drakensteyn, after which the King and his family moved to the newly renovated monarch's palace of Huis ten Bosch in The Hague in 2019.
Willem-Alexander has a villa near Kranidi, Greece.
Villa in Machangulo

On 10 July 2008, the Prince of Orange and Princess Máxima announced that they had invested in a development project on the Mozambican peninsula of Machangulo.
In 2009, controversy erupted in parliament and the press about the project and the prince's involvement.
Politician Alexander Pechtold questioned the morality of building such a resort in a poor country like Mozambique.
Titles, styles, honours and arms

Titles and styles

Willem-Alexander's full title is: His Majesty King Willem-Alexander, King of the Netherlands, Prince of Orange-Nassau, etc., etc., etc.
Willem-Alexander is the first Dutch king since Willem III (d. 1890).
Willem-Alexander had earlier indicated that when he became king, he would take the name Willem IV, but it was announced in January 2013 that his regnal name would be Willem-Alexander.
Military ranks

Royal Netherlands Navy

Royal Netherlands Air Force

Royal Netherlands Army

Royal Marechaussee

Qualifications

Honours

Willem-Alexander has been awarded with the following distinctions:


National

Foreign

Awards

Honorary appointment

Arms

Ancestry

Through his father, a member of the House of Amsberg, he is descended from families of the lower German nobility, and through his mother, from several royal German–Dutch families such as the House of Lippe, Mecklenburg-Schwerin, the House of Orange-Nassau, Waldeck and Pyrmont, and the House of Hohenzollern.
He is descended from the first king of the Netherlands, William I of the Netherlands, who was also a ruler in Luxembourg and several German states, and all subsequent Dutch monarchs.
Through his mother, Willem-Alexander also descends from Paul I of Russia and thus from German princess Catherine the Great and Swedish King Gustav I. Through his father, he is also descended from several Dutch–Flemish families who left the Low Countries during Spanish rule, such as the Berenbergs.
Willem-Alexander is a descendant of King George II and, more relevant for his succession rights, of his granddaughter Princess Augusta of Great Britain.
Under the British Act of Settlement, King Willem-Alexander temporarily forfeited his (distant) succession rights to the throne of the United Kingdom by marrying a Roman Catholic.
Finally, Willem-Alexander is also a distant descendent of William the Silent, who is held to be the Father of the Nation in the Netherlands, since John William Friso, a great-great-grandson of William the Silent, is known to be a common ancestor to all current European monarchs.
Notes

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (aae44f5a-be91-47fa-af25-c8fe79e4de82)
 Call ID: aae44f5a-be91-47fa-af25-c8fe79e4de82
  Args:
    source: Beatrix
    type: :Woman
  AssignClass (9b80f340-f825-4aed-805e-3ecf503cb222)
 Call ID: 9b80f340-f825-4aed-805e-3ecf503cb222
  Args:
    type: :Woman
    source: Margriet
  AssignClass (770845b0-4a8d-4ec3-a51b-b9c6715feead)
 Call ID: 770845b0-4a8d-4ec3-a51b-b9c6715feead
  Args:
    type: :Man
    source: Pieter_van_Vollenhoven
  AssignClass (f34271dc-b4f1-47ed-99b0-288aca6a765c)
 Call ID: f34271dc-b4f1-47ed-99b0-288aca6a765c
  Args:
    source: Willem-Alexander
    type: :Man
  AssignClass (4d938a27-511b-4255-9781-0fa87eb71a7f)
 Call ID: 4d938a27-511b-4255-9781-0fa87eb71a7f
  Args:
    type: :Woman
    source: Juliana
  AssignClass (6ee621b1-3ff2-4084-b5c2-c92b33166d3f)
 Call ID: 6ee621b1-3ff2-4084-b5c2-c92b33166d3f
  Args:
    type: :Man
    source: Claus
  AssignClass (5aaf3dbc-d638-4667-b4eb-dd25cc5bd40c)
 Call ID: 5aaf3dbc-d638-4667-b4eb-dd25cc5bd40c
  Args:
    type: :Woman
    source: Máxima_Zorreguieta_Cerruti
  AssignClass (cb34aaaf-48d6-4ad3-803d-ee4e2bf80cf5)
 Call ID: cb34aaaf-48d6-4ad3-803d-ee4e2bf80cf5
  Args:
    source: Catharina-Amalia
    type: :Woman
  AssignClass (2e59276e-37a3-4341-8c12-c4fd7c21ef88)
 Call ID: 2e59276e-37a3-4341-8c12-c4fd7c21ef88
  Args:
    source: Alexia
    type: :Woman
  AssignClass (10c5d51f-4087-43b8-bbbc-9c090d80b918)
 Call ID: 10c5d51f-4087-43b8-bbbc-9c090d80b918
  Args:
    source: Ariane
    type: :Woman
  AssignClass (241c414b-7ef9-49bb-b43b-776f7c0197af)
 Call ID: 241c414b-7ef9-49bb-b43b-776f7c0197af
  Args:
    type: :Man
    source: William_III
  AssignClass (b6cbd83d-1d90-46b1-bec7-254431440138)
 Call ID: b6cbd83d-1d90-46b1-bec7-254431440138
  Args:
    type: :Woman
    source: Wilhelmina
  AssignClass (99f77136-028e-421a-bfc6-da90350dc660)
 Call ID: 99f77136-028e-421a-bfc6-da90350dc660
  Args:
    source: Bernhard
    type: :Man
  AssignClass (5e1d4752-fdde-4490-a959-369ba8196f76)
 Call ID: 5e1d4752-fdde-4490-a959-369ba8196f76
  Args:
    type: :Man
    source: Friso
  AssignClass (8b97bf31-2da6-4e0e-9462-e75be5e73777)
 Call ID: 8b97bf31-2da6-4e0e-9462-e75be5e73777
  Args:
    source: Constantijn
    type: :Man
  AddLiteral (8d494777-ca8c-40dd-a95a-616124e589a9)
 Call ID: 8d494777-ca8c-40dd-a95a-616124e589a9
  Args:
    literal_type: xsd:integer
    source: Willem-Alexander
    literal_value: 1967
    relation: :hasBirthYear
  AddTriple (62e6b7b4-679e-4a7d-925e-7ee9f598fb81)
 Call ID: 62e6b7b4-679e-4a7d-925e-7ee9f598fb81
  Args:
    source: Willem-Alexander
    target: Beatrix
    relation: :hasMother
  AddTriple (7aa6a62d-30c6-4d15-b63e-5a725bae8742)
 Call ID: 7aa6a62d-30c6-4d15-b63e-5a725bae8742
  Args:
    relation: :hasFather
    source: Willem-Alexander
    target: Claus
  AddTriple (6b689517-310a-46f7-aca9-119dae75563e)
 Call ID: 6b689517-310a-46f7-aca9-119dae75563e
  Args:
    source: Beatrix
    target: Juliana
    relation: :hasMother
  AddTriple (e20ba475-c594-4df2-ab33-112154916fe4)
 Call ID: e20ba475-c594-4df2-ab33-112154916fe4
  Args:
    target: Bernhard
    source: Beatrix
    relation: :hasFather
  AddTriple (ddcf128c-2a3c-41d1-b87e-bb6256644fa5)
 Call ID: ddcf128c-2a3c-41d1-b87e-bb6256644fa5
  Args:
    relation: :hasChild
    target: Catharina-Amalia
    source: Willem-Alexander
  AddTriple (7611301f-1c71-47b4-ab21-2360f1b00170)
 Call ID: 7611301f-1c71-47b4-ab21-2360f1b00170
  Args:
    relation: :hasChild
    source: Willem-Alexander
    target: Alexia
  AddTriple (fcf41a14-318e-49f9-8438-255e294670a2)
 Call ID: fcf41a14-318e-49f9-8438-255e294670a2
  Args:
    source: Willem-Alexander
    target: Ariane
    relation: :hasChild
  AddTriple (5d6a6e35-9472-41f1-9ff5-61f0b8e7ac09)
 Call ID: 5d6a6e35-9472-41f1-9ff5-61f0b8e7ac09
  Args:
    target: Catharina-Amalia
    source: Máxima_Zorreguieta_Cerruti
    relation: :hasChild
  AddTriple (078a9368-d016-4403-99f1-93fbb7297771)
 Call ID: 078a9368-d016-4403-99f1-93fbb7297771
  Args:
    source: Máxima_Zorreguieta_Cerruti
    target: Alexia
    relation: :hasChild
  AddTriple (b5e1d149-28ed-447d-8c86-45bcc3a8765f)
 Call ID: b5e1d149-28ed-447d-8c86-45bcc3a8765f
  Args:
    source: Máxima_Zorreguieta_Cerruti
    target: Ariane
    relation: :hasChild
  AddTriple (5e79cfbf-9a17-4d1a-a2bf-9648d32530cf)
 Call ID: 5e79cfbf-9a17-4d1a-a2bf-9648d32530cf
  Args:
    relation: :hasBrother
    target: Friso
    source: Willem-Alexander
  AddTriple (123b6089-1d3f-45ea-89a1-79ac4e1df573)
 Call ID: 123b6089-1d3f-45ea-89a1-79ac4e1df573
  Args:
    relation: :hasBrother
    target: Constantijn
    source: Willem-Alexander
  AddTriple (2ac0f637-6b03-4528-82ea-c0b39fd0c75e)
 Call ID: 2ac0f637-6b03-4528-82ea-c0b39fd0c75e
  Args:
    relation: :hasMother
    target: Beatrix
    source: Friso
  AddTriple (c46be15c-10be-40ca-9ed5-ceb429d7390d)
 Call ID: c46be15c-10be-40ca-9ed5-ceb429d7390d
  Args:
    relation: :hasFather
    target: Claus
    source: Friso
  AddTriple (cad1d645-b0df-4932-a913-6275c0553065)
 Call ID: cad1d645-b0df-4932-a913-6275c0553065
  Args:
    relation: :hasMother
    target: Beatrix
    source: Constantijn
  AddTriple (630facdf-bd6a-44a1-9c17-bb32f40fe7ff)
 Call ID: 630facdf-bd6a-44a1-9c17-bb32f40fe7ff
  Args:
    relation: :hasFather
    source: Constantijn
    target: Claus
  Finish (8d1a0fe5-68c0-4373-b168-5fa0f8809326)
 Call ID: 8d1a0fe5-68c0-4373-b168-5fa0f8809326
  Args: