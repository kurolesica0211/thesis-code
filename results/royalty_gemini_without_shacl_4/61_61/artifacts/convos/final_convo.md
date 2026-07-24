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
  AssignClass (a08a4e55-9248-4cc7-b174-bda41baa9cef)
 Call ID: a08a4e55-9248-4cc7-b174-bda41baa9cef
  Args:
    type: :Man
    source: Willem-Alexander
  AssignClass (bd719b24-afe8-466a-81a6-5aeed4c6a3b4)
 Call ID: bd719b24-afe8-466a-81a6-5aeed4c6a3b4
  Args:
    type: :Woman
    source: Beatrix
  AssignClass (0d760d77-3699-427e-adb1-727e080a36db)
 Call ID: 0d760d77-3699-427e-adb1-727e080a36db
  Args:
    source: Claus
    type: :Man
  AssignClass (83dd4fce-6ac1-4c06-be46-c5ff970987c3)
 Call ID: 83dd4fce-6ac1-4c06-be46-c5ff970987c3
  Args:
    source: Juliana
    type: :Woman
  AssignClass (92ce1bc8-2f2a-481b-a056-f3efd6698c68)
 Call ID: 92ce1bc8-2f2a-481b-a056-f3efd6698c68
  Args:
    source: Bernhard
    type: :Man
  AssignClass (52d62f98-3917-4849-bdb3-913f66e6ed08)
 Call ID: 52d62f98-3917-4849-bdb3-913f66e6ed08
  Args:
    type: :Woman
    source: Máxima Zorreguieta Cerruti
  AssignClass (5cd4a254-4747-486a-915e-2fadb729ff57)
 Call ID: 5cd4a254-4747-486a-915e-2fadb729ff57
  Args:
    source: Catharina-Amalia
    type: :Woman
  AssignClass (f397ba4f-100f-423d-8d4f-0807b676e073)
 Call ID: f397ba4f-100f-423d-8d4f-0807b676e073
  Args:
    type: :Woman
    source: Alexia
  AssignClass (d057b5cc-d9a3-4343-b0e8-5e631777098b)
 Call ID: d057b5cc-d9a3-4343-b0e8-5e631777098b
  Args:
    type: :Woman
    source: Ariane
  AssignClass (bb6881c0-2068-4c8e-8388-85566f8464d2)
 Call ID: bb6881c0-2068-4c8e-8388-85566f8464d2
  Args:
    type: :Man
    source: Friso
  AssignClass (b76d6777-e577-4d82-9586-0475d999a464)
 Call ID: b76d6777-e577-4d82-9586-0475d999a464
  Args:
    source: Constantijn
    type: :Man
  AddLiteral (86623adb-9f94-4b33-8744-e7b12f8d702e)
 Call ID: 86623adb-9f94-4b33-8744-e7b12f8d702e
  Args:
    relation: :hasBirthYear
    literal_value: 1967
    source: Willem-Alexander
    literal_type: xsd:positiveInteger
  AddTriple (cb3b8569-1b2b-4ec1-adcd-06276f06e1ea)
 Call ID: cb3b8569-1b2b-4ec1-adcd-06276f06e1ea
  Args:
    source: Willem-Alexander
    relation: :hasMother
    target: Beatrix
  AddTriple (99718b2d-36cb-4cd6-b090-ae14eecf0b6d)
 Call ID: 99718b2d-36cb-4cd6-b090-ae14eecf0b6d
  Args:
    target: Claus
    relation: :hasFather
    source: Willem-Alexander
  AddTriple (cd7cd5a7-9b58-4975-82c8-2e7c2a4e69bd)
 Call ID: cd7cd5a7-9b58-4975-82c8-2e7c2a4e69bd
  Args:
    source: Beatrix
    target: Juliana
    relation: :hasMother
  AddTriple (0c222758-cc7d-4f85-861b-461b6e395b91)
 Call ID: 0c222758-cc7d-4f85-861b-461b6e395b91
  Args:
    source: Beatrix
    relation: :hasFather
    target: Bernhard
  AddTriple (12caee7f-21e5-4786-b8a5-c17d716b0e61)
 Call ID: 12caee7f-21e5-4786-b8a5-c17d716b0e61
  Args:
    source: Willem-Alexander
    target: Catharina-Amalia
    relation: :hasChild
  AddTriple (80f2ecf2-82ba-4894-a9d8-44890bf09558)
 Call ID: 80f2ecf2-82ba-4894-a9d8-44890bf09558
  Args:
    source: Willem-Alexander
    relation: :hasChild
    target: Alexia
  AddTriple (e9f8eb34-88ec-4982-a49b-f0b0419a4d60)
 Call ID: e9f8eb34-88ec-4982-a49b-f0b0419a4d60
  Args:
    target: Ariane
    relation: :hasChild
    source: Willem-Alexander
  AddTriple (1917eef1-2225-42ab-a3c6-6f6aee91e78c)
 Call ID: 1917eef1-2225-42ab-a3c6-6f6aee91e78c
  Args:
    source: Máxima Zorreguieta Cerruti
    target: Catharina-Amalia
    relation: :hasChild
  AddTriple (ebe9009c-3fe5-4ddd-b4f8-d18a2699fd05)
 Call ID: ebe9009c-3fe5-4ddd-b4f8-d18a2699fd05
  Args:
    relation: :hasChild
    target: Alexia
    source: Máxima Zorreguieta Cerruti
  AddTriple (f33d67b1-88aa-4b29-beea-bc00053fe258)
 Call ID: f33d67b1-88aa-4b29-beea-bc00053fe258
  Args:
    source: Máxima Zorreguieta Cerruti
    target: Ariane
    relation: :hasChild
  AddTriple (afd75fbb-8581-4d48-8063-e2896dbc2210)
 Call ID: afd75fbb-8581-4d48-8063-e2896dbc2210
  Args:
    source: Willem-Alexander
    relation: :isSiblingOf
    target: Friso
  AddTriple (44c3509a-92bb-4d4d-b545-948242195444)
 Call ID: 44c3509a-92bb-4d4d-b545-948242195444
  Args:
    relation: :isSiblingOf
    target: Constantijn
    source: Willem-Alexander
  Finish (e838f5ae-058c-40b3-ae83-08a4813dbadb)
 Call ID: e838f5ae-058c-40b3-ae83-08a4813dbadb
  Args: